import os

def generate_crud_for_model(model_name: str):
    template = f"""
from sqlalchemy.orm import Session
from .models import {model_name}
from fastapi_auto import create_instance, read_instance, update_instance, delete_instance

def create_{model_name.lower()}(session: Session, model: {model_name}):
    return create_instance(session, {model_name}, **model.dict())

def get_{model_name.lower()}(session: Session, id: int):
    return read_instance(session, {model_name}, id)

def update_{model_name.lower()}(session: Session, id: int, model: {model_name}):
    return update_instance(session, {model_name}, id, **model.dict())

def delete_{model_name.lower()}(session: Session, id: int):
    return delete_instance(session, {model_name}, id)
"""
    return template

def main():
    models_path = 'models'
    crud_path = 'crud'
    
    # Ensure CRUD directory exists
    if not os.path.exists(crud_path):
        os.makedirs(crud_path)
    
    for filename in os.listdir(models_path):
        if filename.endswith('.py') and filename != '__init__.py':
            model_name = filename[:-3]
            
            with open(f"{crud_path}/{model_name}_crud.py", 'w') as f:
                f.write(generate_crud_for_model(model_name))

if __name__ == "__main__":
    main()

