from typing import Annotated

from fastapi import Depends

from eft_item_helper.auth.services import get_current_user
from eft_item_helper.user.schemas import UserSchema


CurrentUserDep = Annotated[UserSchema, Depends(get_current_user)]
