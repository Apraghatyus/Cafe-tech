from repositories.auth_repository import AuthRepository
from models.auth import Auth

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def authenticate(self, username: str, password: str) -> Auth | None:
        user = self.repo.get_by_username(username)
        # En lugar de check_password, comparamos en claro:
        if user and user.password == password:
            return user
        return None
