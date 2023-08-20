from sqlalchemy.orm import sessionmaker, Session
from fastpydantic import pydantic_to_sqlalchemy, set_to_cache, get_from_cache

def create_instance(session: Session, model, **kwargs):
    sqlalchemy_model = pydantic_to_sqlalchemy(model)
    instance = sqlalchemy_model(**kwargs)
    session.add(instance)
    session.commit()
    return instance

def read_instance(session: Session, model, id):
    sqlalchemy_model = pydantic_to_sqlalchemy(model)
    instance = session.query(sqlalchemy_model).filter_by(id=id).first()

    # Cache handling
    cache_key = f"{model.__name__.lower()}:{id}"
    if instance:
        set_to_cache(cache_key, instance)
    else:
        instance = get_from_cache(cache_key)

    return instance

def update_instance(session: Session, model, id, **kwargs):
    sqlalchemy_model = pydantic_to_sqlalchemy(model)
    instance = session.query(sqlalchemy_model).filter_by(id=id).first()
    if instance:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()

        # Invalidate cache
        cache_key = f"{model.__name__.lower()}:{id}"
        set_to_cache(cache_key, instance)
        
    return instance

def delete_instance(session: Session, model, id):
    sqlalchemy_model = pydantic_to_sqlalchemy(model)
    instance = session.query(sqlalchemy_model).filter_by(id=id).first()
    if instance:
        session.delete(instance)
        session.commit()

        # Invalidate cache
        cache_key = f"{model.__name__.lower()}:{id}"
        set_to_cache(cache_key, None)

    return instance

