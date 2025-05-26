from ninja import Router
from django.contrib.auth.models import User
from ninja import Schema
from typing import Optional

api = Router(tags=["users"])
class UserCreateSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@api.post("/auth/register/", response=UserSchema)
def register(request, data: UserCreateSchema):
    if User.objects.filter(username=data.username).exists():
        return api.create_response(request, {"error": "Username already exists"}, status=400)

    if User.objects.filter(email=data.email).exists():
        return api.create_response(request, {"error": "Email already exists"}, status=400)

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return user
