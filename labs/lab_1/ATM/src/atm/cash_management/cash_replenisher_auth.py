from ..authentication.authentication_service import AuthenticationService


class CashReplenisherAuthenticator:
    """Authenticates incassator for cash management."""

    def __init__(self, auth_service: AuthenticationService) -> None:
        self.auth_service = auth_service

    def authenticate(self, user_id: str, pin: str) -> bool:
        """Authenticate incassator (simulated with client auth)."""
        return self.auth_service.authenticate(user_id, pin)
