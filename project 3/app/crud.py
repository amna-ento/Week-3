from sqlalchemy.orm import Session
from app.security import hash_password
from app import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()


def create_user(db: Session, user: schemas.UserCreate):

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)   
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, username: str, password: str):

    user = get_user_by_username(db, username)

    if not user:
        return None

    from app.security import verify_password

    if not verify_password(password, user.password):
        return None

    return user