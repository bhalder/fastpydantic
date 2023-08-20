from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from fastpydantic.boilerplate.db import Base 

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="tokens")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model = Column(String, index=True)  # This will store model name like "User"
    action = Column(String)  # CRUD operations: Create, Read, Update, Delete
    
    user = relationship("User", back_populates="permissions")

