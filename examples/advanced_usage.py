"""Advanced usage examples for SocialConnect library."""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from socialconnect import EmailMessenger, WhatsAppMessenger
from socialconnect.config import SocialConnectConfig
from socialconnect.core.exceptions import SocialConnectError
import logging
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


def advanced_email_example():
    """Advanced email usage with custom configuration."""
    print("=== Advanced Email Example ===")
    
    # Create custom configuration
    config = SocialConnectConfig()
    config.update_email_config(
        sender_email=os.getenv("GMAIL_ADDRESS"),
        password=os.getenv("GMAIL_APP_PASSWORD"),
    )
    
    # Initialize with custom config
    email_messenger = EmailMessenger(
        sender_email=config.email.sender_email,
        password=config.email.password
    )
    
    # Batch processing example
    clients_data = [
        {
            'client_name': 'Client 1',
            'phone_number': '+1234567890',
            'chat_description': 'Interested in studio apartment',
            'unit_details': {'project_name': 'Project A', 'unit_type': 'Studio'},
            'client_request': 'Budget conscious buyer'
        },
        {
            'client_name': 'Client 2', 
            'phone_number': '+0987654321',
            'chat_description': 'Looking for family apartment',
            'unit_details': {'project_name': 'Project B', 'unit_type': '3-Bedroom'},
            'client_request': 'Needs parking space'
        }
    ]
    
    # Process multiple clients
    for i, client_data in enumerate(clients_data):
        try:
            result = email_messenger.send_message(
                client_data=client_data,
                email_addresses=[f"agent{i+1}@company.com"]
            )
            print(f"Client {i+1} processed: {result['statistics']['success_rate']}% success")
        except SocialConnectError as e:
            print(f"Error processing client {i+1}: {e}")


def advanced_whatsapp_example():
    """Advanced WhatsApp usage with error handling."""
    print("=== Advanced WhatsApp Example ===")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize with custom settings
    whatsapp_messenger = WhatsAppMessenger(delay=3)
    
    # Define customer segments
    high_value_customers = [
        {
            'customer_info': {
                'name': 'VIP Client',
                'phone': '+1111111111',
                'chat_summary': 'High budget luxury seeker'
            },
            'unit_info': {
                'unit_id': 'LUX-001',
                'type': 'Penthouse',
                'project': 'Luxury Towers',
                'price': '$1,000,000',
                'unit_availability': 'Limited'
            }
        }
    ]
    
    regular_customers = [
        {
            'customer_info': {
                'name': 'Regular Client',
                'phone': '+2222222222',
                'chat_summary': 'Standard apartment seeker'
            },
            'unit_info': {
                'unit_id': 'STD-001',
                'type': 'Apartment',
                'project': 'Standard Complex',
                'price': '$200,000',
                'unit_availability': 'Available'
            }
        }
    ]
    
    # Process high-value customers with priority
    for customer_data in high_value_customers:
        try:
            # Send to management group for high-value clients
            result = whatsapp_messenger.send_message(
                customer_info=customer_data['customer_info'],
                unit_info=customer_data['unit_info'],
                recipients=os.getenv("WHATSAPP_GROUP_ID"),
                message_type="group"
            )
            print(f"High-value client alert sent: {result['statistics']}")
        except Exception as e:
            print(f"Failed to send high-value alert: {e}")
    
    
    
    # Process regular customers
    sales_agents = ["+201003869531", "+201129563904"]
    
    for customer_data in regular_customers:
        try:
            result = whatsapp_messenger.send_message(
                customer_info=customer_data['customer_info'],
                unit_info=customer_data['unit_info'],
                recipients=sales_agents,
                message_type="individual"
            )
            print(f"Regular client alerts sent: {result['statistics']}")
        except Exception as e:
            print(f"Failed to send regular alerts: {e}")


def error_handling_example():
    """Example of comprehensive error handling."""
    print("=== Error Handling Example ===")
    
    try:
        # This will raise AuthenticationError if no credentials
        email_messenger = EmailMessenger()
    except SocialConnectError as e:
        print(f"Authentication error: {e}")
        # Fallback to environment variables or manual input
        email_messenger = EmailMessenger("fallback@example.com", "password")
    
    # Test with invalid data
    invalid_client_data = {
        'client_name': None,  # Invalid
        'phone_number': 'invalid-phone',  # Invalid
        'unit_details': {}  # Empty
    }
    
    result = email_messenger.send_message(
        client_data=invalid_client_data,
        email_addresses=["invalid-email"]  # Invalid
    )
    
    # Check results and handle failures
    for email, result_data in result['results'].items():
        if not result_data['success']:
            print(f"Failed to send to {email}: {result_data['error']}")
    
    print(f"Overall success rate: {result['statistics']['success_rate']}%")


if __name__ == "__main__":
    advanced_email_example()
    advanced_whatsapp_example()
    error_handling_example()