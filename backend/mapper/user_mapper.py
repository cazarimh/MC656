from ..database.models import User
from ..dto.user_dto import UserRegisterResponse, UserResponse


class UserMapper:
    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(id=user.user_id, email=user.user_email)

    @staticmethod
    def to_register_response(user: User, message: str) -> UserRegisterResponse:
        return UserRegisterResponse(message=message, user=UserMapper.to_response(user))
