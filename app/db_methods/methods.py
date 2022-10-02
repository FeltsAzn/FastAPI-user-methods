from app.config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi import HTTPException
from starlette import status


def async_session_generator():
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    async_session = sessionmaker(bind=engine.connect(), class_=AsyncSession)

    return async_session


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except Exception as _ex:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
    finally:
        await session.close()