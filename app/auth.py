from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from starlette import status
from datetime import datetime

from app.models import AuthToken
from app.db_methods.methods import Database #get_session


async def check_auth_token(token: str, database=Depends(Database)):
    start_db_session = database.async_session_generator()

    async with await start_db_session as session:
        db_response = await database.query(session, AuthToken, AuthToken.token, token)

        if db_response is not None:
            date = await token_time_validity(db_response.created_date)
            if date:
                return db_response
            try:
                await database.delete_data(session, db_response)
            except Exception as ex:
                raise ex
            else:
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
