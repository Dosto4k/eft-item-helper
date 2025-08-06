#!/usr/bin/env -S uv run --script

import sys

import uvicorn
from fastapi import FastAPI

from db import create_all_table
from quest_item.services import fill_db_tables_related_quests_items
from quest_item import views
from auth.views import router as auth_router


app = FastAPI()
app.include_router(views.router)
app.include_router(auth_router)


if __name__ == "__main__":
    create_all_table()
    if "--fill-db" in sys.argv:
        fill_db_tables_related_quests_items()
    else:
        uvicorn.run("main:app", reload=True)
