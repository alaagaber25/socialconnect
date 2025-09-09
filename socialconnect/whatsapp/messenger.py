"""Simplified WhatsApp messenger implementation with essential functionality."""

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
    """Simplified WhatsApp messaging system for sales teams."""
    
    def __init__(self, delay: int = 5, close_tab: bool = True):
        """
        Initialize the messenger with settings.
        
        Args:
            delay: Default delay between actions in seconds
            close_tab: Whether to close WhatsApp tabs after sending
        """
        super().__init__("WhatsAppMessenger")
        self.delay = delay
        self.close_tab = close_tab
        self.formatter = MessageFormatter()
        
    def validate_config(self) -> bool:
        """Validate WhatsApp messenger configuration."""
        # WhatsApp messenger doesn't need special configuration
        return True
    
    def send_message(self, customer_info: Dict, unit_info: Dict, 
                    recipients: Union[str, List[str]], 
                    message_type: str = "individual") -> Dict[str, Any]:
        """
        Send customer interest message to recipients (groups or individuals).
        
        Args:
            customer_info: Customer information
            unit_info: Unit information  
            recipients: Group ID(s) or phone number(s) - can be string or list
            message_type: "group" or "individual"
            
        Returns:
            Dictionary with send results and statistics
        """
        # Convert single recipient to list for uniform processing
        if isinstance(recipients, str):
            recipients = [recipients]
        
        if not recipients:
            raise ValidationError("At least one recipient must be provided")
        
        # Validate message type
        if message_type.lower() not in ["group", "individual"]:
            raise ValidationError(f"Invalid message_type: {message_type}. Must be 'group' or 'individual'")
        
        is_group = message_type.lower() == "group"
        
        # Create message
        message = self.formatter.create_customer_interest_message(customer_info, unit_info)
        
        # Process all recipients
        results = {}
        successful_sends = 0
        
        for i, recipient in enumerate(recipients):
            self.logger.info(f"Sending to {recipient} ({i+1}/{len(recipients)})")
            
            try:
                # Validate recipient based on type
                if not recipient:
                    raise ValidationError("Recipient cannot be empty")
                
                if not is_group and not validate_phone_number(recipient):
                    raise ValidationError(f"Invalid phone number format: {recipient}")
                
                # Copy message to clipboard
                pyperclip.copy(message)
                
                # Send message based on recipient type
                if is_group:
                    kit.sendwhatmsg_to_group_instantly(recipient, " ")
                    recipient_type = "group"
                else:
                    kit.sendwhatmsg_instantly(recipient, " ")
                    recipient_type = "individual"
                
                # Wait for WhatsApp to load
                time.sleep(self.delay)
                
                # Paste and send message
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("enter")
                time.sleep(1)
                
                # Close WhatsApp tab if configured
                if self.close_tab:
                    pyautogui.hotkey("ctrl", "w")
                    time.sleep(0.5)
                
                self._log_success(recipient, f"WhatsApp {recipient_type} message")
                results[recipient] = {
                    'success': True,
                    'error': None,
                    'timestamp': datetime.now().isoformat(),
                    'type': recipient_type
                }
                successful_sends += 1
                
                # Add delay between messages to avoid rate limiting
                if i < len(recipients) - 1:  # Don't delay after the last message
                    time.sleep(2)
                    
            except Exception as e:
                self._log_error(recipient, str(e), "WhatsApp message")
                results[recipient] = {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat(),
                    'type': 'group' if is_group else 'individual'
                }
        
        # Calculate statistics
        total_sends = len(recipients)
        success_rate = (successful_sends / total_sends) * 100 if total_sends > 0 else 0
        
        self.logger.info(f"WhatsApp sending complete: {successful_sends}/{total_sends} successful")
        
        return {
            'results': results,
            'statistics': {
                'total_sent': total_sends,
                'successful': successful_sends,
                'failed': total_sends - successful_sends,
                'success_rate': round(success_rate, 2),
                'recipient_type': message_type.lower()
            },
            'timestamp': datetime.now().isoformat()
        }