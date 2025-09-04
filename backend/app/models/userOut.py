from pydantic import BaseModel, Field

class UserOut(BaseModel):
    id: int
    email: str