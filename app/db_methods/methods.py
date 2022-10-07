from app.config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from app.models import User

from app.users.schemas import CreateUserForm


class Database:
    @staticmethod
    async def async_session_generator():
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return async_session

    async def query(self, table, first_arg, second_arg):
        session = await self.async_session_generator()
        s = session()
        query = select(table).where(first_arg == second_arg)
        database_response = await s.execute(query)
        result = database_response.scalar()
        return result, s

    @staticmethod
    async def add(session, data):
        try:
            session.add(data)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            await session.close()
            return True
        finally:
            await session.close()

    @staticmethod
    async def create(db_response, session, new_data):
        if db_response:
            await session.close()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        try:
            session.add(new_data)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            await session.close()
            return {'User': f'Created user {new_data.email}'}
        finally:
            await session.close()

    @staticmethod
    async def delete(db_response, session):
        if db_response:
            await session.close()
            return {'detail': 'This user does not exist'}
        try:
            session.delete(db_response)
            await session.commit()
        except Exception as _ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            await session.close()
            return True
        finally:
            await session.close()







