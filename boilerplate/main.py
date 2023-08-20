from fastapi_auto import auto_route, init, init_redis
from .models import User

init("sqlite:///./test.db")
init_redis()

auto_route(User)

