from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from starlette import status
from datetime import datetime

from app.models import AuthToken
from app.db_methods.methods import Database #get_session


async def check_auth_token(token: str, database=Depends(Database)):
    db_resp, session = database.query(AuthToken, AuthToken.token, token)
    async with database as session:
        query = select(AuthToken).where(AuthToken.token == token)
        result = await database.execute(query)
        auth_token = result.scalar()
        if auth_token is not None:
            date = await token_time_validity(auth_token.created_date)
            if date:
                return auth_token
            else:
                await session.delete(auth_token)
                raise HTTPException(status_code=status.HTTP_423_LOCKED, detail='Auth token expired')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


async def token_time_validity(auth_token_time: datetime.now()):
    """Check time for token in database"""
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_check = int(time_now[11:13])*60 + int(time_now[14:16])
    token_time = int(auth_token_time[11:13])*60 + int(auth_token_time[14:16])
    valid = True if time_check - token_time <= 60 else False
    if auth_token_time[:10] == time_now[:10] and valid:
        return True
    return False
