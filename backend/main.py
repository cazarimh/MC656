from fastapi import FastAPI, HTTPException, status
from .models import UserCreate, UserOut
from .password_hash import get_password_hash
from .validators import validate_email_format, validate_password_strength

app = FastAPI()

dict_db = {}
user_id = 0

@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    global user_id

    validate_email_format(user_data.email)

    validate_password_strength(user_data.password)

    for user in dict_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está cadastrado."
            )
        
    hashed_password = get_password_hash(user_data.password)
    user_id += 1
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password
    }

    dict_db[new_user["id"]] = new_user

    return new_user