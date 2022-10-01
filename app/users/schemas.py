from pydantic import BaseModel, validator
from string import ascii_lowercase, digits, ascii_uppercase


class UserLoginForm(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class CreateUserForm(BaseModel):
    email: str
    password: str
    nickname: str = None

    @validator('email')
    def check_mail(cls, mail):
        if '@' not in mail and ' ' in mail:
            raise ValueError('Invalid email!')
        return mail

    @validator('password')
    def check_password(cls, pw):
        # if pw in database_easy_pass:
        #     raise ValueError('Too easy password!')
        up_state = False
        low_state = False
        num_state = False
        for letter in pw:
            if letter in ascii_uppercase:
                up_state = True
            elif letter in ascii_lowercase:
                low_state = True
            elif letter in digits:
                num_state = True

        if all([up_state, low_state, num_state]) and 20 >= len(pw) >= 8:
            return pw
        raise ValueError('Invalid password!')

    class Config:
        orm_mode = True


class UpdateUserForm(CreateUserForm, BaseModel):
    email: str = None
    password: str = None
    nickname: str = None

    class Config:
        orm_mode = True
