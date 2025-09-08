"""Tests for WhatsApp messenger functionality."""

import pytest
from unittest.mock import patch, MagicMock
from socialconnect import WhatsAppMessenger
from socialconnect.core.exceptions import ValidationError


class TestWhatsAppMessenger:
    """Test cases for WhatsAppMessenger class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.customer_info = {
            'name': 'John Smith',
            'phone': '+1234567890',
            'chat_summary': 'Interested in 2-bedroom apartment'
        }
        
        self.unit_info = {
            'unit_id': 'UNIT-001',
            'type': 'Apartment',
            'project': 'Sunset Villas',
            'price': '$250,000',
            'unit_availability': 'Available'
        }
    
    def test_messenger_initialization(self):
        """Test messenger initialization."""
        messenger = WhatsAppMessenger(delay=3)
        assert messenger.delay == 3
        assert messenger.validate_config() is True
    
    def test_send_single_message_validation_error(self):
        """Test validation error when no recipient provided."""
        messenger = WhatsAppMessenger()
        
        result = messenger._send_single_message("Test message")
        assert result is False
    
    def test_send_single_message_invalid_phone(self):
        """Test validation error for invalid phone number."""
        messenger = WhatsAppMessenger()
        
        result = messenger._send_single_message("Test message", phone_number="invalid")
        assert result is False
    
    @patch('socialconnect.whatsapp.messenger.kit.sendwhatmsg_to_group_instantly')
    @patch('socialconnect.whatsapp.messenger.pyperclip.copy')
    @patch('socialconnect.whatsapp.messenger.pyautogui')
    @patch('socialconnect.whatsapp.messenger.time.sleep')
    def test_send_to_group_success(self, mock_sleep, mock_pyautogui, mock_copy, mock_kit):
        """Test successful group message sending."""
        messenger = WhatsAppMessenger()
        
        result = messenger.send_to_group(
            self.customer_info, 
            self.unit_info, 
            "test_group_id"
        )
        
        assert result['statistics']['successful'] == 1
        assert result['statistics']['success_rate'] == 100.0
        mock_copy.assert_called_once()
        mock_kit.assert_called_once()
    
    @patch('socialconnect.whatsapp.messenger.kit.sendwhatmsg_instantly')
    @patch('socialconnect.whatsapp.messenger.pyperclip.copy')
    @patch('socialconnect.whatsapp.messenger.pyautogui')
    @patch('socialconnect.whatsapp.messenger.time.sleep')
    def test_send_to_individuals_success(self, mock_sleep, mock_pyautogui, mock_copy, mock_kit):
        """Test successful individual message sending."""
        messenger = WhatsAppMessenger()
        
        result = messenger.send_to_individuals(
            self.customer_info,
            self.unit_info,
            ["+1234567890", "+0987654321"]
        )
        
        assert result['statistics']['total_sent'] == 2
        assert mock_kit.call_count == 2