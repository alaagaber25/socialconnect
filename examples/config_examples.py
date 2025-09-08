"""Configuration examples for SocialConnect library."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from socialconnect.config import SocialConnectConfig


def basic_config_example():
    """Basic configuration setup."""
    print("=== Basic Configuration ===")
    
    # Load configuration from environment
    config = SocialConnectConfig()
    
    # Display current configuration
    print("Current configuration:")
    config_dict = config.to_dict()
    for section, settings in config_dict.items():
        print(f"\n{section.upper()}:")
        for key, value in settings.items():
            # Don't print sensitive information
            if 'password' in key.lower():
                value = "***hidden***" if value else None
            print(f"  {key}: {value}")


def custom_config_example():
    """Custom configuration setup."""
    print("=== Custom Configuration ===")
    
    config = SocialConnectConfig()
    
    # Update email configuration from environment
    config.update_email_config(
        sender_email=os.getenv("GMAIL_ADDRESS"),
        password=os.getenv("GMAIL_APP_PASSWORD"),
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=int(os.getenv("SMTP_PORT", 587))
    )
    
    # Update WhatsApp configuration from environment
    config.update_whatsapp_config(
        delay=int(os.getenv("WHATSAPP_DELAY", 3)),
        close_tab=os.getenv("WHATSAPP_CLOSE_TAB", "false").lower() == "true"
    )
    
    print("Updated configuration:")
    config_dict = config.to_dict()
    for section, settings in config_dict.items():
        print(f"\n{section.upper()}:")
        for key, value in settings.items():
            if 'password' in key.lower():
                value = "***configured***" if value else None
            print(f"  {key}: {value}")


def environment_config_example():
    """Environment-based configuration."""
    print("=== Environment Configuration ===")
    
    # Check if required environment variables are set
    required_env_vars = ['GMAIL_ADDRESS', 'GMAIL_APP_PASSWORD']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the example.")
        return
    
    # Load configuration
    config = SocialConnectConfig()
    
    print("Configuration loaded from environment:")
    print(f"Email: {config.email.sender_email}")
    print(f"SMTP Server: {config.email.smtp_server}")
    print(f"SMTP Port: {config.email.smtp_port}")
    print(f"WhatsApp Delay: {config.whatsapp.delay}")


if __name__ == "__main__":
    basic_config_example()
    print("\n" + "="*50 + "\n")
    custom_config_example()
    print("\n" + "="*50 + "\n")
    environment_config_example()