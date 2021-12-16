"""
Will hold pydantic models

# Example of a User Model

class User(BaseModel):
    id: UUID = uuid4()
    username: constr(min_length=3)
    admin: bool
    email: EmailStr
    fullname: Optional[str] = None
    disabled: Optional[bool] = False
    scope: Scope
    last_connection: Optional[Union[str, pendulum.DateTime]] = None
"""
from pydantic import BaseModel


class Server(BaseModel):
    id: str
