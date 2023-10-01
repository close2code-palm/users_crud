import functools
import re
from enum import Enum
from typing import Optional, TypeVar, Literal

from pydantic import BaseModel, EmailStr, ValidationError, field_validator, model_validator


OrderingType = TypeVar('OrderingType', Literal['username'], Literal['email'])


class Ordering(str, Enum):
    USERNAME: OrderingType = 'username'
    EMAIL: OrderingType = 'email'


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None

    @field_validator('password')
    @classmethod
    def secure_password(cls, password):
        if len(password) < 9:
            raise ValidationError('Password is too short!')
        password_validations = functools.partial(re.match, string=password)
        for reg in ['.*[A-Z].*', '.*[a-z].*', '.*[0-9].*', '.*[^A-Za-z0-9].*']:
            if not password_validations(reg):
                raise ValidationError('To be secure, your password must '
                                      'contain capital and lowercase letters,'
                                      ' numbers and special characters!')
        return password


class UserUpdateModel(UserCreateModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @model_validator(mode='after')
    def validate(self) -> 'UserUpdateModel':
        if not any((self.email, self.password, self.username)):
            raise ValidationError('At list one field must be provided')
        return self


class UserDBModel(UserCreateModel):
    user_id: int
