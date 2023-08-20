from sqlalchemy.orm import Session
from fastpydantic.boilerplate.models.auth import AuthMixin

def requires_auth(model):
    return issubclass(model, AuthMixin)

def get_current_user(db: Session, token: str):
    db_token = db.query(Token).filter(Token.token == token).first()
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    return db_token.user
