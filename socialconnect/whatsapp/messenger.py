"""WhatsApp messenger implementation."""

import pywhatkit as kit
import pyperclip
import pyautogui
import time
from datetime import datetime
from typing import Dict, List, Union, Any

from ..core.base import BaseMessenger
from ..core.exceptions import MessagingError, ValidationError
from ..utils.validators import validate_phone_number
from .formatters import MessageFormatter


class WhatsAppMessenger(BaseMessenger):
    """A WhatsApp messaging system for sales teams to send customer interest alerts."""
    
    def __init__(self, delay: int = 5):
        """
        Initialize the messenger with settings.
        
        Args:
            delay: Default delay between actions in seconds
        """
        super().__init__("WhatsAppMessenger")
        self.delay = delay
        self.formatter = MessageFormatter()
        
    def validate_config(self) -> bool:
        """Validate WhatsApp messenger configuration."""
        # WhatsApp messenger doesn't need special configuration
        return True
    
    def _send_single_message(self, message: str, group_id: str = None, 
                           phone_number: str = None) -> bool:
        """
        Base method for sending WhatsApp messages.
        
        Args:
            message: Message content to send
            group_id: WhatsApp group ID (for group messages)
            phone_number: Phone number (for individual messages)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not group_id and not phone_number:
                raise ValidationError("Either group_id or phone_number must be provided")
            
            if phone_number and not validate_phone_number(phone_number):
                raise ValidationError(f"Invalid phone number format: {phone_number}")
            
            # Copy message to clipboard
            pyperclip.copy(message)
            
            # Send message based on recipient type
            if group_id:
                kit.sendwhatmsg_to_group_instantly(group_id, " ")
                recipient = f"group {group_id}"
            else:
                kit.sendwhatmsg_instantly(phone_number, " ")
                recipient = phone_number
            
            # Wait for WhatsApp to load
            time.sleep(self.delay)
            
            # Paste and send message
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            time.sleep(2)
            
            # Close WhatsApp tab
            pyautogui.hotkey("ctrl", "w")
            
            self._log_success(recipient, "WhatsApp message")
            return True
            
        except Exception as e:
            recipient = group_id or phone_number or "unknown"
            self._log_error(recipient, str(e), "WhatsApp message")
            return False
    
    def send_to_group(self, customer_info: Dict, unit_info: Dict, group_id: str) -> Dict[str, Any]:
        """
        Send customer interest alert to a WhatsApp group.
        
        Args:
            customer_info: Customer information
            unit_info: Unit information
            group_id: WhatsApp group ID to send the message to
            
        Returns:
            Dictionary with send results
        """
        message = self.formatter.create_customer_interest_message(customer_info, unit_info)
        success = self._send_single_message(message, group_id=group_id)
        
        return {
            'results': {group_id: {'success': success, 'error': None if success else 'Send failed'}},
            'statistics': {
                'total_sent': 1,
                'successful': 1 if success else 0,
                'failed': 0 if success else 1,
                'success_rate': 100.0 if success else 0.0
            }
        }
    
    def send_to_individuals(self, customer_info: Dict, unit_info: Dict, 
                          phone_numbers: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Send customer interest alert to individual(s).
        
        Args:
            customer_info: Customer information
            unit_info: Unit information
            phone_numbers: Single phone number or list of phone numbers
            
        Returns:
            Dictionary with send results and statistics
        """
        if isinstance(phone_numbers, str):
            phone_numbers = [phone_numbers]
        
        message = self.formatter.create_customer_interest_message(customer_info, unit_info)
        results = {}
        
        for phone_number in phone_numbers:
            try:
                success = self._send_single_message(message, phone_number=phone_number)
                results[phone_number] = {'success': success, 'error': None}
                # Small delay between individual messages to avoid issues
                time.sleep(2)
            except Exception as e:
                results[phone_number] = {'success': False, 'error': str(e)}
        
        # Calculate statistics
        successful_sends = sum(1 for r in results.values() if r['success'])
        total_sends = len(results)
        
        return {
            'results': results,
            'statistics': {
                'total_sent': total_sends,
                'successful': successful_sends,
                'failed': total_sends - successful_sends,
                'success_rate': (successful_sends / total_sends) * 100 if total_sends > 0 else 0
            }
        }
    
    def send_message(self, customer_info: Dict, unit_info: Dict, 
                    recipients: Union[str, List[str]], 
                    message_type: str = "individual") -> Dict[str, Any]:
        """
        Universal send method that handles both groups and individuals.
        
        Args:
            customer_info: Customer information
            unit_info: Unit information  
            recipients: Group ID or phone number(s)
            message_type: "group" or "individual"
            
        Returns:
            Dictionary with send results and statistics
        """
        if message_type == "group":
            if isinstance(recipients, list):
                raise ValidationError("Group messaging only supports single group ID")
            return self.send_to_group(customer_info, unit_info, recipients)
        else:
            return self.send_to_individuals(customer_info, unit_info, recipients)
