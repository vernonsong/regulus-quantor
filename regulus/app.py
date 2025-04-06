# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
import uvicorn
from fastapi import FastAPI
from interfaces.rest import message, strategy

app = FastAPI(root_path='/regulus')
app.include_router(message.router)
app.include_router(strategy.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}

if __name__ == '__main__':
    uvicorn.run('app:app')
