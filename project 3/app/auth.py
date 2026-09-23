from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security import create_access_token
from app.database import get_db
from app import crud, schemas
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



from app.dependencies import get_current_user
from app import models


@router.get("/profile", response_model=schemas.UserResponse)
def profile(
    current_user: models.User = Depends(get_current_user)
):
    return current_user