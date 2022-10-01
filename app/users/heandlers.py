import uuid  # для генерации токена
from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException
from app.users.schemas import UserLoginForm, CreateUserForm, UpdateUserForm
from app.models import connection_db, User, AuthToken
from app.utils import get_password_hash, get_session_token
from app.auth import check_auth_token
from app.db_methods.methods import Database

router = APIRouter()


@router.get('/')
async def index():
    return {'Docs': 'http://127.0.0.1:8000/docs'}


@router.post('/user/login', name='login to service')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(Database)):
    """Login to user account"""
    user = database.session.query(User, AuthToken).join(AuthToken, AuthToken.user_id == User.user_id).filter(User.email == user_form.email).one_or_none()
    # TODO доделать запрос к бд
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'Email or password invalid'}

    # user_token = database.session.query(AuthToken).filter(AuthToken.user_id == user.user_id).one_or_none()
    if user.token is not None:
        # return {'status':'Account already authorized'})
        return {'session_token': f'{user.token}'}

    session_token = AuthToken(token=get_session_token(user.user_id), user_id=user.user_id)
    db_resp = database.add(session_token)
    if db_resp:
        return {'session_token': f'{session_token.token}'}
    HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=db_resp)


@router.post('/user/logout', name='logout from service')
def logout(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    user = database.session.query(User).filter(User.user_id == token.user_id).one()
    email = user.email
    db_resp = database.delete(token)
    if db_resp:
        return {f'user {email}: Logout'}
    HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=db_resp)


@router.post('/user/info')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Getting user information by his token"""
    user = database.session.query(User).filter(User.user_id == token.user_id).one_or_none()
    if user:
        return {'id': user.user_id, 'email': user.email, 'nickname': user.nickname}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.post('/user/create', name='user:create', response_model_exclude_unset=True)
def create_user(user: CreateUserForm = Body(..., embed=True), database=Depends(Database)):
    """To generate the correct password, the following must be used:
    1 digit,
    1 capital letter,
    1 small letter,
    Password length: from 8 to 20 characters,
    Use only latin letters"""
    exists_user = database.session.query(User.user_id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        nickname=user.nickname
    )
    db_resp = database.add(new_user)
    if db_resp:
        return {'User': f'Created user {user.email}'}
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=db_resp)


@router.post('/user/update', response_model_exclude_unset=True)
def update_user(new_user: UpdateUserForm, old_pwd: str = Body(..., embed=True),
                token: AuthToken = Depends(check_auth_token), database=Depends(Database)):
    """Update account information. The correctness of the password and email address is also checked.
    Parameters are optional, can be changed by choice"""
    user = database.query(User).filter(User.user_id == token.user_id).one()
    if user.password == get_password_hash(old_pwd):
        if new_user.email:
            user.email = new_user.email
        if new_user.password:
            user.password = get_password_hash(new_user.password)
        if new_user.nickname:
            user.nickname = new_user.nickname
        db_resp = database.add(user)
        if db_resp:
            return {'status': "Successfully"}
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=db_resp)
    return {'error': 'Wrong old password!'}


@router.post('/user/delete')
def delete_user(old_pwd: str = Body(..., embed=True), token: AuthToken = Depends(check_auth_token),
                database=Depends(Database)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    user = database.session.query(User).filter(User.user_id == token.user_id).one()
    if user:
        email = user.email
        if get_password_hash(old_pwd) == user.password:
            db_resp_token = database.delete(token)
            db_resp_user = database.delete(user)
            if db_resp_token and db_resp_user:
                return {f'user {email}: Deleted'}
            raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                detail=(not db_resp_token or not db_resp_user))
        return {'error': 'Wrong old password!'}
    return {'answer': 'This user does not exist'}

