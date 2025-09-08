"""Custom exceptions for SocialConnect library."""


class SocialConnectError(Exception):
    """Base exception for all SocialConnect errors."""
    pass


class MessagingError(SocialConnectError):
    """Raised when message sending fails."""
    pass


class AuthenticationError(SocialConnectError):
    """Raised when authentication fails."""
    pass


class ValidationError(SocialConnectError):
    """Raised when validation fails."""
    pass


class ConfigurationError(SocialConnectError):
    """Raised when configuration is invalid."""
    pass