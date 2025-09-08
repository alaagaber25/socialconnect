"""Configuration settings for SocialConnect library."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EmailConfig:
    """Email configuration settings."""
    sender_email: Optional[str] = None
    password: Optional[str] = None
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    use_ssl: bool = True


@dataclass
class WhatsAppConfig:
    """WhatsApp configuration settings."""
    delay: int = 5
    close_tab: bool = True


class SocialConnectConfig:
    """Main configuration class for SocialConnect library."""
    
    def __init__(self):
        self.email = EmailConfig()
        self.whatsapp = WhatsAppConfig()
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Email configuration
        self.email.sender_email = os.getenv("GMAIL_ADDRESS")
        self.email.password = os.getenv("GMAIL_APP_PASSWORD")
        self.email.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.email.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        
        # WhatsApp configuration
        self.whatsapp.delay = int(os.getenv("WHATSAPP_DELAY", "5"))
    
    def update_email_config(self, **kwargs):
        """Update email configuration."""
        for key, value in kwargs.items():
            if hasattr(self.email, key):
                setattr(self.email, key, value)
    
    def update_whatsapp_config(self, **kwargs):
        """Update WhatsApp configuration."""
        for key, value in kwargs.items():
            if hasattr(self.whatsapp, key):
                setattr(self.whatsapp, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'email': {
                'sender_email': self.email.sender_email,
                'smtp_server': self.email.smtp_server,
                'smtp_port': self.email.smtp_port,
                'use_ssl': self.email.use_ssl
            },
            'whatsapp': {
                'delay': self.whatsapp.delay,
                'close_tab': self.whatsapp.close_tab
            }
        }