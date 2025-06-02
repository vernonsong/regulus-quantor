import argparse
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession
from mcp.client.streamable_http import logger, streamablehttp_client
from openai import AsyncOpenAI


class MCPClient:

    def __init__(self, server_url: str, model: str = 'gpt-4.1-nano'):

        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI(
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
            api_key='',
        )
        self.model = model
        self.server_url = server_url
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self):

        # Connect to the server using streamable HTTP
        streamable_transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(self.server_url))
        read_stream, write_stream, _ = streamable_transport

        # Create session with streamable HTTP transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream))

        # Initialize the connection
        await self.session.initialize()

        # List available tools
        tools_result = await self.session.list_tools()
        logger.info('\nConnected to streaming server with tools:')
        for tool in tools_result.tools:
            logger.info(f" - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:

        tools_result = await self.session.list_tools()
        return [{
            'type': 'function',
            'function': {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.inputSchema,
            },
        } for tool in tools_result.tools]

    async def process_query(self, query: str) -> str:
        """
        Process a user query using OpenAI and available MCP tools.

        The process follows these steps:
        1. Get available tools from the server
        2. Send initial query to OpenAI
        3. If tool calls are needed:
           - Execute each tool call
           - Get final response with tool results
        4. Return the final response

        Args:
            query (str): The user's input query

        Returns:
            str: The final response from OpenAI

        Note:
            This implementation can be replaced with a workflow engine like
            Langgraph for more complex processing patterns.
        """
        # Get available tools
        tools = await self.get_mcp_tools()

        # Initial OpenAI API call
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{
                'role': 'user',
                'content': query
            }],
            tools=tools,
            tool_choice='auto',
            temperature=0.1)

        # Get assistant's response
        assistant_message = response.choices[0].message

        # Initialize conversation with user query and assistant response
        messages = [
            {
                'role': 'user',
                'content': query
            },
            assistant_message,
        ]

        # Handle tool calls if present
        if assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                # Execute tool call
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )

                # Add tool response to conversation
                messages.append({
                    'role': 'tool',
                    'tool_call_id': tool_call.id,
                    'content': result.content[0].text,
                })

            # Get final response from OpenAI with tool results
            final_response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice='none',  # Don't allow more tool calls
            )

            return final_response.choices[0].message.content

        # No tool calls, just return the direct response
        return assistant_message.content

    async def cleanup(self):
        """
        Clean up resources and close connections.

        This method ensures proper cleanup of all async resources
        managed by the exit stack.
        """
        await self.exit_stack.aclose()


async def main(args):
    """
    Main entry point for the client application.

    This function:
    1. Creates an MCP client instance
    2. Connects to the streaming server
    3. Enters an interactive loop for processing queries
    4. Handles cleanup on exit

    Args:
        args: Command line arguments containing server_url and model
    """
    client = MCPClient(args.server_url, args.model)
    await client.connect_to_server()

    try:
        while True:
            print('--------------------------------\n')
            query = input('Enter a query: ')
            response = await client.process_query(query)
            print(f"Response: {response}")
            print('--------------------------------\n')
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt detected, exiting...')
    finally:
        await client.cleanup()


if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='OpenAI MCP Client - Interactive tool-enabled chat client')
    parser.add_argument(
        '--server-url',
        type=str,
        default='http://localhost:8000/mcp',
        help='URL of the MCP server (default: http://localhost:8001/mcp)',
    )
    parser.add_argument(
        '--model',
        type=str,
        default='qwen-plus',
        help='OpenAI model to use (default: gpt-4.1-nano)',
    )
    args = parser.parse_args()
    asyncio.run(main(args))
