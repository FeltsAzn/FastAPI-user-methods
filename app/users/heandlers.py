from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException
from app.users.schemas import UserLoginForm, CreateUserForm, UpdateUserForm
from app.users.models import User, AuthToken
from app.utils import get_password_hash, get_session_token, check_new_info
from app.auth import check_auth_token
from app.db_methods.methods import Database

router = APIRouter()


@router.get('/')
async def index():
    return {'Docs': 'http://127.0.0.1:8000/docs'}


@router.post('/user/login', name='login to service', status_code=202)
async def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(Database)):
    """Login to user account"""
    start_db_session = database.async_session_generator()

    async with await start_db_session as session:
        user = await database.query(session, User, User.email, user_form.email)
        if user is None or await get_password_hash(user_form.password) != user.password:
            return {'error': 'Email or password invalid'}

        old_user_token = await database.query(session, AuthToken, AuthToken.user_id, user.user_id)

        new_session_token = AuthToken(token=await get_session_token(user.user_id), user_id=user.user_id)
        try:
            await database.delete_data(session, old_user_token)
            await database.add(session, new_session_token)
        except Exception as _ex:
            raise _ex
        else:
            return {'session_token': f'{new_session_token.token}'}


@router.post('/user/logout', name='logout from service', status_code=202)
async def logout(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    start_db_session = await database.async_session_generator()
    async with start_db_session as session:
        user = await database.query(session, User, User.user_id, token.user_id)
        email = user.email
        try:
            await database.delete_data(session, token)
        except Exception as _ex:
            raise _ex
        else:
            return {f'user {email}: Logout'}


@router.post('/user/info')
async def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Getting user information by his token"""
    start_db_session = await database.async_session_generator()
    async with start_db_session as session:
        user = database.query(session, User, User.user_id, token.user_id)
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
        password=await get_password_hash(user.password),
        nickname=user.nickname)
    start_db_session = await database.async_session_generator()
    async with start_db_session as session:
        try:
            db_resp = await database.query(session, User, User.email, user.email)
            await database.create(session, db_resp, new_user)
        except Exception as ex:
            raise ex
        else:
            return {'User': f'Created user {new_user.email}'}


@router.put('/user/update', response_model_exclude_unset=True)
async def update_user(new_user: UpdateUserForm, old_pwd: str = Body(..., embed=True),
                      token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Update account information. The correctness of the password and email address is also checked.
    Parameters are optional, can be changed by choice"""
    start_db_session = await database.async_session_generator()
    async with start_db_session as session:
        user = await database.query(session, User, User.user_id, token.user_id)
        update_user = await check_new_info(user, new_user, old_pwd)
        if update_user:
            try:
                await database.add(session, update_user)
            except Exception as _ex:
                raise _ex
            else:
                return {'status': "Successfully"}
        return {'error': 'Wrong old password!'}


@router.delete('/user/delete', status_code=202)
async def delete_user(old_pwd: str = Body(..., embed=True), token: AuthToken = Depends(check_auth_token),
                      database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    start_db_session = await database.async_session_generator()
    async with start_db_session as session:

        user = database.query(session, User, User.user_id, token.user_id)
        if user is not None:
            email = user.email
            if await get_password_hash(old_pwd) == user.password:
                try:
                    await database.delete_data(session, token)
                    await database.delete_data(session, user)
                except Exception as _ex:
                    raise _ex
                else:
                    return {f'user {email}: Deleted'}

            return {'error': 'Wrong old password!'}


