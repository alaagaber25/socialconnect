"""Tests for email messenger functionality."""

import pytest
import os
from unittest.mock import patch, MagicMock
from socialconnect import EmailMessenger
from socialconnect.core.exceptions import AuthenticationError, ValidationError


class TestEmailMessenger:
    """Test cases for EmailMessenger class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_client_data = {
            'client_name': 'Ahmed Hassan',
            'phone_number': '+20 12 3456 7890',
            'chat_description': 'Client contacted via WhatsApp expressing interest.',
            'unit_details': {
                'project_name': 'New Capital Heights',
                'unit_type': '2-Bedroom Apartment',
                'unit_number': 'A-205',
                'size': '120 sqm',
                'price': '2,800,000 EGP',
                'floor': '2nd Floor'
            },
            'inquiry_time': '2024-12-15 14:30:00',
            'client_request': 'Interested in flexible payment plan.'
        }
    
    def test_messenger_initialization_with_credentials(self):
        """Test messenger initialization with provided credentials."""
        messenger = EmailMessenger("test@example.com", "password123")
        assert messenger.sender_email == "test@example.com"
        assert messenger.password == "password123"
    
    def test_messenger_initialization_without_credentials(self):
        """Test messenger initialization without credentials raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthenticationError):
                EmailMessenger()
    
    @patch.dict(os.environ, {'GMAIL_ADDRESS': 'test@gmail.com', 'GMAIL_APP_PASSWORD': 'password'})
    def test_messenger_initialization_from_env(self):
        """Test messenger initialization from environment variables."""
        messenger = EmailMessenger()
        assert messenger.sender_email == 'test@gmail.com'
        assert messenger.password == 'password'
    
    def test_validate_config(self):
        """Test configuration validation."""
        messenger = EmailMessenger("test@example.com", "password123")
        assert messenger.validate_config() is True
        
        messenger.sender_email = None
        assert messenger.validate_config() is False
    
    @patch('socialconnect.email.messenger.smtplib.SMTP_SSL')
    def test_send_single_email_success(self, mock_smtp):
        """Test successful single email sending."""
        messenger = EmailMessenger("test@example.com", "password123")
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = messenger._send_single_email(self.sample_client_data, "recipient@example.com")
        
        assert result is True
        mock_server.login.assert_called_once_with("test@example.com", "password123")
        mock_server.send_message.assert_called_once()
    
    def test_send_single_email_invalid_email(self):
        """Test sending to invalid email address."""
        messenger = EmailMessenger("test@example.com", "password123")
        
        result = messenger._send_single_email(self.sample_client_data, "invalid-email")
        assert result is False
    
    @patch('socialconnect.email.messenger.smtplib.SMTP_SSL')
    def test_send_message_multiple_recipients(self, mock_smtp):
        """Test sending message to multiple recipients."""
        messenger = EmailMessenger("test@example.com", "password123")
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        emails = ["recipient1@example.com", "recipient2@example.com"]
        result = messenger.send_message(self.sample_client_data, emails)
        
        assert result['statistics']['total_sent'] == 2
        assert result['statistics']['successful'] == 2
        assert result['statistics']['success_rate'] == 100.0
