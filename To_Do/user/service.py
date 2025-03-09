from .repositories import UserRepository
from .Dtos.create_user_dto import UserCreate, UserResponse

class UserService:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def create_user(self, user: UserCreate):
        return self.user_repo.create_user(user)

    def get_user(self, user_id: int):
        return self.user_repo.get_user(user_id)

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.user_repo.get_users(skip, limit)