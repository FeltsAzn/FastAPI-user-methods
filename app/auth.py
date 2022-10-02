from fastapi import Depends, HTTPException
from starlette import status
from datetime import datetime

from app.models import AuthToken
from app.db_methods.methods import get_session


async def check_auth_token(token: str, database=Depends(get_session)):
    async with database() as session:
        auth_token = await session.query(AuthToken).filter(AuthToken.token == token).one_or_none()
        if auth_token:
            if token_time_validity(auth_token.created_date):
                return auth_token
            else:
                await session.delete(auth_token)
                raise HTTPException(status_code=status.HTTP_423_LOCKED, detail='Auth token expired')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


async def token_time_validity(auth_token_time: datetime.now()):
    """Check time for token in database"""
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if auth_token_time[:10] == time_now[:10] and auth_token_time[11:13] == time_now[11:13]:
        return True
    return False
