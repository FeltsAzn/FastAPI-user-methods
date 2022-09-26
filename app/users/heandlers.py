import uuid  # для генерации токена
from starlette import status
from fastapi import APIRouter, Body, Depends, HTTPException
from app.users.schemas import UserLoginForm, CreateUserForm, UpdateUserForm
from app.models import connection_db, User, AuthToken
from app.utils import get_password_hash
from app.auth import check_auth_token


router = APIRouter()


@router.get('/')
async def index():
    return {'Docs': 'http://127.0.0.1:8000/docs'}


@router.post('/user/login', name='login to service')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connection_db)):
    """Login to user account"""
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'Email or password invalid'}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.user_id)
    token = auth_token.token
    try:
        database.add(auth_token)
        database.commit()
    except Exception as _ex:
        return {'error': _ex}
    finally:
        database.close()
    return {'auth_token': f'{token}'}


@router.post('/user/logout', name='logout from service')
def logout(token: AuthToken = Depends(check_auth_token), database=Depends(connection_db)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    user = database.query(User).filter(User.user_id == token.user_id).one()
    email = user.email
    try:
        database.delete(token)
        database.commit()
    except Exception as _ex:
        return {'error': _ex}
    finally:
        database.close()

    return {f'user {email}: Logout'}


@router.get('/user/info')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connection_db)):
    """Getting user information by his token"""
    user = database.query(User).filter(User.user_id == token.user_id).one_or_none()
    return {'id': user.user_id, 'email': user.email, 'nickname': user.nickname}


@router.post('/user/create', name='user:create', response_model_exclude_unset=True)
def create_user(user: CreateUserForm = Body(..., embed=True), database=Depends(connection_db)):
    """To generate the correct password, the following must be used:
    1 digit,
    1 capital letter,
    1 small letter,
    Password length: from 8 to 20 characters,
    Use only latin letters"""
    exists_user = database.query(User.user_id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        nickname=user.nickname
    )
    user_id = new_user.user_id
    try:
        database.add(new_user)
        database.commit()
    except Exception as _ex:
        return {'error': _ex}
    finally:
        database.close()

    return {'User': f'Created user {user_id}'}


@router.put('/user', response_model_exclude_unset=True)
def update_user(new_user: UpdateUserForm, token: AuthToken = Depends(check_auth_token), database=Depends(connection_db)):
    """Update account information. The correctness of the password and email address is also checked.
    Parameters are optional, can be changed by choice"""
    user = database.query(User).filter(User.user_id == token.user_id).one()
    if new_user.email:
        user.email = new_user.email
    if new_user.password:
        user.password = get_password_hash(new_user.password)
    if new_user.nickname:
        user.nickname = new_user.nickname
    try:
        database.add(user)
        database.commit()
    except Exception as _ex:
        return {'error': _ex}
    finally:
        database.close()
    return {'status': "Successfully"}


@router.delete('/user')
def delete_user(token: AuthToken = Depends(check_auth_token), database=Depends(connection_db)):
    """Removing a user from the database by authorization token (to protect against removal from outside)"""
    user = database.query(User).filter(User.user_id == token.user_id).one()
    if user:
        email = user.email
        try:
            database.delete(user)
            database.commit()
        except Exception as _ex:
            return {'error': _ex}
        finally:
            database.close()
        return {f'user {email}: Deleted'}
    return {'answer': 'This user does not exist'}

