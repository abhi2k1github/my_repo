from pydantic import BaseModel
from typing import Optional, Union, ClassVar
from uuid import UUID


class CreateUser(BaseModel):
    name: str
    email: str
    mobile_number: str
    mobile_country_code: str
    password: str
    status: str

class LoginUser(BaseModel):
    email: str
    password: str
    auth_scope: str
  