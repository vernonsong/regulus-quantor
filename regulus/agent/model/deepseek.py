# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from typing import Dict, Optional, Union

from langchain_core.outputs import ChatResult
from langchain_deepseek import ChatDeepSeek


# todo 改为log
class DeepSeek(ChatDeepSeek):
    """
    DeepSeek模型
    """

    def _generate(self, prompts, **kwargs):
        print('=== Prompts ===')
        for prompt in prompts:
            print(prompt)
        return super()._generate(prompts, **kwargs)

    def _create_chat_result(
        self,
        response: Union[dict],
        generation_info: Optional[Dict] = None,
    ) -> ChatResult:
        print('=== Reasion Content ===')
        print(response.choices[0].message.reasoning_content)
        return super()._create_chat_result(response, generation_info)
