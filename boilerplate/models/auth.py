from pydantic import BaseModel

class AuthMixin(BaseModel):
    token: str

