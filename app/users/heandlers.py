import uuid  # для генерации токена
from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException
from app.users.schemas import UserLoginForm, CreateUserForm, UpdateUserForm
from app.models import User, AuthToken
from app.utils import get_password_hash, get_session_token
from app.auth import check_auth_token
from app.db_methods.methods import Database #get_session
from sqlalchemy import select

router = APIRouter()


@router.get('/')
async def index():
    return {'Docs': 'http://127.0.0.1:8000/docs'}


@router.post('/user/login', name='login to service', status_code=202)
async def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(Database)):
    """Login to user account"""
    async with database as session:
        query = select(User).where(User.email == user_form.email)
        result = await database.execute(query)
        user = result.scalar()
        if user is None or await get_password_hash(user_form.password) != user.password:
            return {'error': 'Email or password invalid'}

        q = select(AuthToken).where(AuthToken.user_id == user.user_id)
        res = await database.execute(q)
        user_token = res.scalar()

        session_token = AuthToken(token=await get_session_token(user.user_id), user_id=user.user_id)

        if user_token.token is not None:
            try:
                session.delete(user_token)
                await session.commit()
            except Exception as _ex:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
            else:
                return {'session_token': f'{session_token.token}'}
        try:
            session.add(session_token)
            await session.commit()
        except Exception as _ex:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            return {'session_token': f'{session_token.token}'}


@router.post('/user/logout', name='logout from service', status_code=202)
async def logout(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    async with database as session:
        query = select(User).where(User.user_id == token.user_id)
        result = await database.execute(query)
        user = result.scalar()
        email = user.email
        try:
            session.delete(token)
            await session.commit()
        except Exception as _ex:
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
        else:
            return {f'user {email}: Logout'}


@router.post('/user/info')
async def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Getting user information by his token"""
    async with database:
        query = select(User).where(User.user_id == token.user_id)
        result = await database.execute(query)
        user = result.scalar()
        if user:
            return {'id': user.user_id, 'email': user.email, 'nickname': user.nickname}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.post('/user/create', name='user:create', response_model_exclude_unset=True, status_code=201)
async def create_user(user: CreateUserForm = Body(..., embed=True), database=Depends(Database)):
    """To generate the correct password, the following must be used:
    1 digit,
    1 capital letter,
    1 small letter,
    Password length: from 8 to 20 characters,
    Use only latin letters"""
    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        nickname=user.nickname)
    db_response = await database.create(user, new_user)
    return db_response





@router.put('/user/update', response_model_exclude_unset=True)
async def update_user(new_user: UpdateUserForm, old_pwd: str = Body(..., embed=True),
                      token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Update account information. The correctness of the password and email address is also checked.
    Parameters are optional, can be changed by choice"""
    async with database as session:
        query = select(User).where(User.user_id == token.user_id)
        result = await database.execute(query)
        user = result.scalar()
        if user.password == await get_password_hash(old_pwd):
            if new_user.email:
                user.email = new_user.email
            if new_user.password:
                user.password = await get_password_hash(new_user.password)
            if new_user.nickname:
                user.nickname = new_user.nickname
            try:
                session.add(user)
                await session.commit()
            except Exception as _ex:
                raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
            else:
                return {'status': "Successfully"}
        return {'error': 'Wrong old password!'}


@router.delete('/user/delete', status_code=202)
async def delete_user(old_pwd: str = Body(..., embed=True), token: AuthToken = Depends(check_auth_token),
                      database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    async with database as session:
        query = select(User).where(User.user_id == token.user_id)
        result = await database.execute(query)
        user = result.scalar()
        if user is not None:
            email = user.email
            if await get_password_hash(old_pwd) == user.password:
                try:
                    session.delete(token)
                    session.delete(user)
                    await session.commit()
                except Exception as _ex:
                    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_ex)
                else:
                    return {f'user {email}: Deleted'}

            return {'error': 'Wrong old password!'}

        return {'answer': 'This user does not exist'}
