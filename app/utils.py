import hashlib
import time
from typing import Union

import jwt
from app.config import SECRET_KEY, ALGORITHM, JWT_KEY
from app.models import User
from app.users.schemas import UpdateUserForm


async def get_password_hash(password: str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf-8')).hexdigest()


async def get_session_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "time": time.time()
    }
    return jwt.encode(payload, key=JWT_KEY, algorithm=ALGORITHM)


async def check_new_info(user: User, new_user: UpdateUserForm, old_pwd: str) -> Union[User, bool]:
    old_pwd = await get_password_hash(old_pwd)
    if user.password == old_pwd:
        if new_user.email:
            user.email = new_user.email
        if new_user.password:
            user.password = await get_password_hash(new_user.password)
        if new_user.nickname:
            user.nickname = new_user.nickname
        return user
    return False

