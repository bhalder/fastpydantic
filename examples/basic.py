from fastpydantic import auto_route, init, init_redis
from pydantic import BaseModel

init_redis()

class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    id: int
    name: str
    age: int
    address: Address

auto_route(User)
Session = init("sqlite:///./test.db")

# You can then run your FastAPI application.
# This will have a GET endpoint at `/user/{id}` which will fetch a User based on the ID.
