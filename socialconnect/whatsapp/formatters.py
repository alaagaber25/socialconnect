"""Message formatters for WhatsApp messages."""

from typing import Dict
from datetime import datetime


class MessageFormatter:
    """Handles formatting of various message types for WhatsApp."""
    
    def format_timestamp(self) -> str:
        """Get current timestamp in a readable format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def create_customer_interest_message(self, customer_info: Dict, unit_info: Dict) -> str:
        """
        Create the customer interest message format.
        
        Args:
            customer_info: Customer information
            unit_info: Unit information
            
        Returns:
            Formatted message
        """
        timestamp = self.format_timestamp()
        
        message = f"""🎯 *NEW CUSTOMER INTEREST* 🎯

👤 *Customer Details:*
• Name: {customer_info.get('name', 'N/A')}
• Phone: {customer_info.get('phone', 'N/A')}
• Summary: {customer_info.get('chat_summary', 'N/A')}

🏠 *Unit Information:*
• Unit ID: {unit_info.get('unit_id', 'N/A')}
• Type: {unit_info.get('type', 'N/A')}
• Project: {unit_info.get('project', 'N/A')}
• Price: {unit_info.get('price', 'N/A')}
• Availability: {unit_info.get('unit_availability', 'N/A')}

⏰ *Time:* {timestamp}

💼 *Action Required:* Please follow up with the customer within 2 hours!"""

        return message