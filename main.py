#!/usr/bin/env -S uv run --script

import sys

import uvicorn
from fastapi import FastAPI

from db import create_all_table
from quest_item.services import fill_db_tables_related_quests_items


app = FastAPI()


if __name__ == "__main__":
    if '--fill-db' in sys.argv:
        fill_db_tables_related_quests_items()
    else:
        create_all_table()
        uvicorn.run('main:app', reload=True)
