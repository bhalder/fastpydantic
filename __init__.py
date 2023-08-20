# fastapi_auto/__init__.py

import redis
from fastapi import Depends, HTTPException
import json

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from fastapi import FastAPI
from typing import Type

Base = declarative_base()
app = FastAPI()

# Global Redis connection pool
pool = None

def init_redis(host='localhost', port=6379, db=0):
    global pool
    pool = redis.ConnectionPool(host=host, port=port, db=db)

def get_from_cache(key):
    if pool:
        with redis.Redis(connection_pool=pool) as client:
            value = client.get(key)
            if value:
                return json.loads(value)

def set_to_cache(key, value, expiration=None):
    if pool:
        with redis.Redis(connection_pool=pool) as client:
            client.set(key, json.dumps(value), ex=expiration)

def pydantic_to_sqlalchemy(pydantic_model, models_cache=None):
    if models_cache is None:
        models_cache = {}
        
    attributes = {}
    relationships = {}
    tablename = pydantic_model.__name__.lower()

    # Relationships
    for name, field in pydantic_model.__annotations__.items():
        if isinstance(field, type) and issubclass(field, BaseModel):
            attributes[name + "_id"] = Column(Integer, ForeignKey(f"{field.__name__.lower()}.id"))
            relationships[name] = relationship(field.__name__)
            models_cache[field.__name__] = pydantic_to_sqlalchemy(field, models_cache)

    # Fields
    for name, field in pydantic_model.__fields__.items():
        field_type = field.outer_type_

        if field_type == int:
            attributes[name] = Column(Integer)
        elif field_type == str:
            attributes[name] = Column(String)
        elif field_type == float:
            attributes[name] = Column(Float)
        elif field_type == bool:
            attributes[name] = Column(Boolean)
        # Add more type conversions as needed

    attributes.update(relationships)
    attributes['__tablename__'] = tablename
    
    sqlalchemy_model = type(pydantic_model.__name__, (Base,), attributes)
    models_cache[pydantic_model.__name__] = sqlalchemy_model
    
    return sqlalchemy_model

def auto_route(model: Type[BaseModel]):
    sql_model = pydantic_to_sqlalchemy(model)

    @app.get(f"/{model.__name__.lower()}/{{id}}", response_model=model)
    async def get_item(id: int, session: sessionmaker = Depends()):
        cache_key = f"{model.__name__.lower()}:{id}"

        # Try getting from cache first
        cached_value = get_from_cache(cache_key)
        if cached_value:
            return cached_value

        with session() as db:
            item = db.query(sql_model).filter(sql_model.id == id).first()
            if item:
                set_to_cache(cache_key, item)  # Cache the result
                return item
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")


def init(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)

