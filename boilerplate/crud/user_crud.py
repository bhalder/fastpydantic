
from sqlalchemy.orm import Session
from .models import user
from fastapi_auto import create_instance, read_instance, update_instance, delete_instance

def create_user(session: Session, model: user):
    return create_instance(session, user, **model.dict())

def get_user(session: Session, id: int):
    return read_instance(session, user, id)

def update_user(session: Session, id: int, model: user):
    return update_instance(session, user, id, **model.dict())

def delete_user(session: Session, id: int):
    return delete_instance(session, user, id)
