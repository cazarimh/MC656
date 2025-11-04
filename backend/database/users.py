from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

def create_user_db(db: Session, user: UserCreate):
    new_user = User(user_email=user.email, user_name=user.name, user_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.user_email == user_email).first()

def update_user_email(db: Session, user_id: int, new_email: str):
    user = get_user_by_id(db, user_id)
    if (user):
        user.user_email = new_email
        db.commit()

def update_user_name(db: Session, user_id: int, new_name: str):
    user = get_user_by_id(db, user_id)
    if (user):
        user.user_name = new_name
        db.commit()

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if (user):
        db.delete(user)
        db.commit()