from models.auth import Auth

class AuthRepository:
    def get_by_username(self, username: str) -> Auth | None:
        return Auth.query.filter_by(username=username).first()
