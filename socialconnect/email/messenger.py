"""Email messenger implementation."""

import os
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from typing import List, Union, Dict, Any

from ..core.base import BaseMessenger
from ..core.exceptions import MessagingError, AuthenticationError, ValidationError
from ..utils.validators import validate_email
from .templates import EmailTemplates


class EmailMessenger(BaseMessenger):
    """A class for sending client inquiry emails to individuals or groups."""
    
    def __init__(self, sender_email: str = None, password: str = None):
        """
        Initialize the email messenger.
        
        Args:
            sender_email: Sender's email address (defaults to env variable)
            password: Email password (defaults to env variable)
        """
        super().__init__("EmailMessenger")
        
        self.sender_email = sender_email or os.getenv("GMAIL_ADDRESS")
        self.password = password or os.getenv("GMAIL_APP_PASSWORD")
        self.templates = EmailTemplates()
        
        if not self.validate_config():
            raise AuthenticationError("Email credentials not provided")
    
    def validate_config(self) -> bool:
        """Validate email configuration."""
        return bool(self.sender_email and self.password)
    
    def _send_single_email(self, client_data: Dict, recipient_email: str) -> bool:
        """
        Send email to a single recipient.
        
        Args:
            client_data: Client information dictionary
            recipient_email: Recipient's email address
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not validate_email(recipient_email):
                raise ValidationError(f"Invalid email address: {recipient_email}")
            
            # Get inquiry time or use current time
            inquiry_time = client_data.get('inquiry_time', 
                                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # Create subject line
            project_name = client_data.get('unit_details', {}).get('project_name', 'Property')
            subject = f"New Client Inquiry - {client_data.get('client_name', 'Unknown')} - {project_name}"
            
            # Create HTML and text content
            html_body = self.templates.create_client_inquiry_html(client_data, inquiry_time)
            text_body = self.templates.create_client_inquiry_text(client_data, inquiry_time)
            
            # Create the email message object
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            # Set both HTML and plain text content
            msg.set_content(text_body)
            msg.add_alternative(html_body, subtype='html')
            
            # Create a secure SSL context
            context = ssl.create_default_context()
            
            # Connect to Gmail's SMTP server and send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            
            self._log_success(recipient_email, "email")
            return True
            
        except Exception as e:
            self._log_error(recipient_email, str(e), "email")
            return False
    
    def send_message(self, client_data: Dict, 
                    email_addresses: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Send client inquiry email to individual or multiple recipients.
        
        Args:
            client_data: Dictionary containing client information
            email_addresses: Single email or list of emails
            
        Returns:
            Dictionary with send results and statistics
        """
        if isinstance(email_addresses, str):
            email_addresses = [email_addresses]
        
        results = {}
        
        for email in email_addresses:
            try:
                success = self._send_single_email(client_data, email)
                results[email] = {'success': success, 'error': None}
            except Exception as e:
                results[email] = {'success': False, 'error': str(e)}
        
        # Calculate statistics
        successful_sends = sum(1 for r in results.values() if r['success'])
        total_sends = len(results)
        
        self.logger.info(f"Email sending complete: {successful_sends}/{total_sends} successful")
        
        return {
            'results': results,
            'statistics': {
                'total_sent': total_sends,
                'successful': successful_sends,
                'failed': total_sends - successful_sends,
                'success_rate': (successful_sends / total_sends) * 100 if total_sends > 0 else 0
            }
        }
