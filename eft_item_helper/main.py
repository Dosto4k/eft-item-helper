#!/usr/bin/env -S uv run --script

import sys

import uvicorn
from fastapi import FastAPI

from db import create_all_table
from quest_item.services import fill_db_tables_related_quests_items
from quest_item.views import router as quest_item_router
from auth.views import router as auth_router
from auth.exceptions import InvalidCookieSessionError
from auth.handlers import invalid_cookie_session_handler


app = FastAPI()
app.include_router(quest_item_router)
app.include_router(auth_router)
app.exception_handlers[InvalidCookieSessionError] = invalid_cookie_session_handler


if __name__ == "__main__":
    create_all_table()
    if "--fill-db" in sys.argv:
        fill_db_tables_related_quests_items()
    else:
        uvicorn.run("main:app", reload=True)
