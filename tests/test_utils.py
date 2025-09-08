"""Tests for utility functions."""

import pytest
from socialconnect.utils import validate_email, validate_phone_number, setup_logger


class TestValidators:
    """Test cases for validation utilities."""
    
    def test_validate_email_valid(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "invalid",
            "@example.com",
            "test@",
            "test..test@example.com",
            "",
            None,
            123
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_phone_number_valid(self):
        """Test valid phone numbers."""
        valid_phones = [
            "+1234567890",
            "+44 20 7946 0958",
            "+1 (555) 123-4567",
            "+201234567890"
        ]
        
        for phone in valid_phones:
            assert validate_phone_number(phone) is True
    
    def test_validate_phone_number_invalid(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            "123",
            "+1234",
            "invalid",
            "",
            None,
            123
        ]
        
        for phone in invalid_phones:
            assert validate_phone_number(phone) is False
    
    def test_setup_logger(self):
        """Test logger setup."""
        logger = setup_logger("test_logger")
        assert logger.name == "test_logger"
        assert len(logger.handlers) == 1
