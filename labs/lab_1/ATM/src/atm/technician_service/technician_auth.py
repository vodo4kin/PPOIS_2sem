from ..authentication.authentication_service import AuthenticationService


class TechnicianAuthenticator:
    """Authenticates technician for service operations."""

    def __init__(self, auth_service: AuthenticationService) -> None:
        self.auth_service = auth_service

    def authenticate(self, user_id: str, pin: str) -> bool:
        """Authenticate technician (simulated)."""
        return self.auth_service.authenticate(user_id, pin)
