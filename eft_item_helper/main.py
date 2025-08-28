#!/usr/bin/env -S uv run --script

import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from eft_item_helper.auth.exceptions import InvalidCookieSessionError
from eft_item_helper.auth.handlers import invalid_cookie_session_handler
from eft_item_helper.auth.views import router as auth_router
from eft_item_helper.db import create_all_table
from eft_item_helper.quest_item.services import fill_db_tables_related_quests_items
from eft_item_helper.quest_item.views import router as quest_item_router


app = FastAPI()
app.include_router(quest_item_router)
app.include_router(auth_router)
app.exception_handlers[InvalidCookieSessionError] = invalid_cookie_session_handler
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    create_all_table()
    if "--fill-db" in sys.argv:
        fill_db_tables_related_quests_items()
    else:
        uvicorn.run("main:app", reload=True)
