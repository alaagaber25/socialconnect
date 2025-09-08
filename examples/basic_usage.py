"""Basic usage examples for SocialConnect library."""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from socialconnect import EmailMessenger, WhatsAppMessenger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def email_example():
    """Example of sending emails with SocialConnect."""
    
    print("=== Email Example ===")
    
    # Initialize email messenger
    email_messenger = EmailMessenger()
    
    # Sample client data
    client_data = {
        'client_name': 'Ahmed Hassan',
        'phone_number': '+20 12 3456 7890',
        'chat_description': 'Client contacted via WhatsApp expressing interest in a 2-bedroom apartment.',
        'unit_details': {
            'project_name': 'New Capital Heights',
            'unit_type': '2-Bedroom Apartment',
            'unit_number': 'A-205',
            'size': '120 sqm',
            'price': '2,800,000 EGP',
            'floor': '2nd Floor'
        },
        'inquiry_time': '2024-12-15 14:30:00',
        'client_request': 'Interested in flexible payment plan and site visit.'
    }
    
    # Send to single recipient
    result = email_messenger.send_message(
        client_data=client_data,
        email_addresses="alaasilva25@gmail.com"
    )
    
    print(f"Email Result: {result['statistics']}")
    
    # Send to multiple recipients
    multiple_result = email_messenger.send_message(
        client_data=client_data,
        email_addresses=["alaasilva25@gmail.com", "alaasilva255@gmail.com"]
    )
    
    print(f"Multiple Email Result: {multiple_result['statistics']}")


def whatsapp_example():
    """Example of sending WhatsApp messages with SocialConnect."""
    print("=== WhatsApp Example ===")
    
    # Initialize WhatsApp messenger
    whatsapp_messenger = WhatsAppMessenger(delay=5)
    
    # Sample data
    customer_info = {
        'name': 'John Smith',
        'phone': '+1234567890',
        'chat_summary': 'Interested in 2-bedroom apartment, budget 250k'
    }
    
    unit_info = {
        'unit_id': 'UNIT-001',
        'type': 'Apartment',
        'project': 'Sunset Villas',
        'price': '$250,000',
        'unit_availability': 'Available'
    }
    
    # Send to group
    group_result = whatsapp_messenger.send_to_group(
        customer_info=customer_info,
        unit_info=unit_info,
        group_id=os.getenv("WHATSAPP_GROUP_ID")
    )
    
    print(f"Group Message Result: {group_result['statistics']}")
    
    # Send to individuals
    individual_result = whatsapp_messenger.send_to_individuals(
        customer_info=customer_info,
        unit_info=unit_info,
        phone_numbers=["+201129563904", "+201003869531"]
    )
    
    print(f"Individual Messages Result: {individual_result['statistics']}")


if __name__ == "__main__":
    # Run examples
    email_example()
    whatsapp_example()