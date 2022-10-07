from app.config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from app.models import User

from app.users.schemas import CreateUserForm


# def async_session_generator():
#     engine = create_async_engine(DATABASE_URL, echo=False, future=True)
#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#     return async_session
#
#
# # @asynccontextmanager
# async def get_session():
#     try:
#         async_session = async_session_generator()
#
#         async with async_session() as session:
#             yield session
#     except Exception as _ex:
#         await session.rollback()
#         raise _ex
#     finally:
#         print('Session close')
#         await session.close()


class Database:
    def __init__(self):
        self.session = self.get_session()
    @staticmethod
    def async_session_generator():
        engine = create_async_engine(DATABASE_URL, echo=False, future=True)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return async_session

    async def get_session(self):
        try:
            async_session = self.async_session_generator()

            async with async_session() as session:
                yield session
        except Exception as _ex:
            await session.rollback()
            raise _ex
        finally:
            print('Session close')
            await session.close()

    async def query(self, table, first_arg, second_arg):
        query = select(table).where(first_arg == second_arg)
        database_response = await self.session.execute(query)
        result = database_response.scalar()
        return result

    async def create(self, user_form: CreateUserForm, new_user: User):
        db_resp = self.query(User, User.email, user_form.email)
        print(db_resp)
        if db_resp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        try:
            self.session.add(new_user)
            await self.session.commit()
        except Exception as _ex:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            self.session.close()
            print("session close")
            return {'User': f'Created user {user_form.email}'}






