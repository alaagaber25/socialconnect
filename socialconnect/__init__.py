"""
SocialConnect - A comprehensive social media and messaging library.

This library provides easy-to-use interfaces for sending messages across
various social media and messaging platforms including email and WhatsApp.
"""

from .email.messenger import EmailMessenger
from .whatsapp.messenger import WhatsAppMessenger
from .core.exceptions import (
    SocialConnectError,
    MessagingError,
    AuthenticationError,
    ValidationError
)

__all__ = [
    'EmailMessenger',
    'WhatsAppMessenger',
    'SocialConnectError',
    'MessagingError',
    'AuthenticationError',
    'ValidationError'
]
