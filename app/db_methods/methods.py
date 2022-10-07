from app.config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select


class Database:
    @staticmethod
    async def async_session_generator():
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return async_session()

    @staticmethod
    async def query(session, table, first_arg, second_arg):
        query = select(table).where(first_arg == second_arg)
        database_response = await session.execute(query)
        result = database_response.scalar()
        return result

    @staticmethod
    async def add(session, data):
        try:
            session.add(data)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            return True

    @staticmethod
    async def create(session, db_response, new_data):
        if db_response:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        try:
            session.add(new_data)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            return True

    @staticmethod
    async def delete_data(session, db_response):
        if db_response is None:
            return {'detail': 'This user does not exist'}
        try:
            await session.delete(db_response)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            return True






