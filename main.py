#!/usr/bin/env -S uv run --script

import uvicorn
from fastapi import FastAPI
from db import create_all_table


app = FastAPI()


if __name__ == "__main__":
    create_all_table()
    uvicorn.run('main:app', reload=True)
