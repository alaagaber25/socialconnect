"""Simplified WhatsApp usage examples using only the send_message method."""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from socialconnect import WhatsAppMessenger
from socialconnect.core.exceptions import SocialConnectError, ValidationError
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)


def single_group_example():
    """Example of sending to a single group."""
    print("=== Single Group Example ===")
    
    whatsapp = WhatsAppMessenger(delay=3)
    
    customer_info = {
        'name': 'Ahmed Hassan',
        'phone': '+20123456789',
        'chat_summary': 'Interested in 2-bedroom apartment with garden view'
    }
    
    unit_info = {
        'unit_id': 'APT-205',
        'type': '2-Bedroom Apartment',
        'project': 'Green Valley Residence',
        'price': '2,500,000 EGP',
        'unit_availability': 'Available'
    }
    
    try:
        result = whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=os.getenv("WHATSAPP_GROUP_ID"),
            message_type="group"
        )
        print(f"Single group result: {result['statistics']}")
    except SocialConnectError as e:
        print(f"Single group send failed: {e}")


def single_individual_example():
    """Example of sending to a single individual."""
    print("=== Single Individual Example ===")
    
    whatsapp = WhatsAppMessenger(delay=3)
    
    customer_info = {
        'name': 'Sarah Mohamed',
        'phone': '+201234567890',
        'chat_summary': 'Looking for studio apartment near metro station'
    }
    
    unit_info = {
        'unit_id': 'STD-101',
        'type': 'Studio Apartment',
        'project': 'Metro Heights',
        'price': '1,800,000 EGP',
        'unit_availability': 'Available'
    }
    
    try:
        result = whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients="+201129563904",
            message_type="individual"
        )
        print(f"Single individual result: {result['statistics']}")
    except SocialConnectError as e:
        print(f"Single individual send failed: {e}")


def multiple_groups_example():
    """Example of sending to multiple groups."""
    print("=== Multiple Groups Example ===")
    
    whatsapp = WhatsAppMessenger(delay=3)
    
    # High-value client requiring management attention
    high_value_customer = {
        'name': 'Omar Khalil',
        'phone': '+201987654321',
        'chat_summary': 'High-budget client seeking luxury penthouse - URGENT'
    }
    
    luxury_unit = {
        'unit_id': 'PH-001',
        'type': 'Penthouse',
        'project': 'Elite Towers',
        'price': '8,000,000 EGP',
        'unit_availability': 'Exclusive - Last Unit'
    }
    
    # Multiple management groups
    management_groups = [
        os.getenv("WHATSAPP_GROUP_ID"),
        "LcSS6CfDnJo7flzShRMlSm_BACKUP"  # Example backup group
    ]
    
    try:
        result = whatsapp.send_message(
            customer_info=high_value_customer,
            unit_info=luxury_unit,
            recipients=management_groups,
            message_type="group"
        )
        print(f"Multiple groups result: {result['statistics']}")
        
        # Show detailed results
        for group, details in result['results'].items():
            status = "✅ Success" if details['success'] else f"❌ Failed: {details['error']}"
            print(f"  {group}: {status}")
            
    except SocialConnectError as e:
        print(f"Multiple groups send failed: {e}")


def multiple_individuals_example():
    """Example of sending to multiple individuals."""
    print("=== Multiple Individuals Example ===")
    
    whatsapp = WhatsAppMessenger(delay=3)
    
    customer_info = {
        'name': 'Fatma Ali',
        'phone': '+201555777888',
        'chat_summary': 'Family looking for 3-bedroom apartment with parking'
    }
    
    unit_info = {
        'unit_id': 'FAM-301',
        'type': '3-Bedroom Apartment',
        'project': 'Family Gardens',
        'price': '3,200,000 EGP',
        'unit_availability': 'Available with parking'
    }
    
    # Sales team members
    sales_team = [
        "+201129563904",
        "+201003869531", 
        "+201555666777"
    ]
    
    try:
        result = whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=sales_team,
            message_type="individual"
        )
        print(f"Multiple individuals result: {result['statistics']}")
        
        # Show detailed results
        for agent, details in result['results'].items():
            status = "✅ Success" if details['success'] else f"❌ Failed: {details['error']}"
            print(f"  {agent}: {status}")
            
    except SocialConnectError as e:
        print(f"Multiple individuals send failed: {e}")


def error_handling_example():
    """Example of error handling with invalid recipients."""
    print("=== Error Handling Example ===")
    
    whatsapp = WhatsAppMessenger(delay=2)
    
    customer_info = {
        'name': 'Test Customer',
        'phone': '+201111111111',
        'chat_summary': 'Test inquiry for error handling demonstration'
    }
    
    unit_info = {
        'unit_id': 'TEST-001',
        'type': 'Test Unit',
        'project': 'Test Project',
        'price': '1,000,000 EGP',
        'unit_availability': 'Testing'
    }
    
    # Mix of valid and invalid phone numbers
    mixed_recipients = [
        "+201129563904",  # Valid
        "invalid-phone",  # Invalid format
        "+201003869531",  # Valid
        "",               # Empty string
        "+201555666777"   # Valid
    ]
    
    try:
        result = whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=mixed_recipients,
            message_type="individual"
        )
        
        print(f"Error handling result: {result['statistics']}")
        print("\nDetailed results:")
        
        for recipient, details in result['results'].items():
            if details['success']:
                print(f"  ✅ {recipient}: Message sent successfully")
            else:
                print(f"  ❌ {recipient}: Failed - {details['error']}")
                
    except ValidationError as e:
        print(f"Validation error: {e}")
    except SocialConnectError as e:
        print(f"General error: {e}")


def workflow_example():
    """Example showing a complete workflow with different message types."""
    print("=== Complete Workflow Example ===")
    
    whatsapp = WhatsAppMessenger(delay=3)
    
    # Premium investment opportunity
    investment_customer = {
        'name': 'Mohamed Abdelrahman',
        'phone': '+201888999000',
        'chat_summary': 'Investment client interested in multiple units for rental portfolio'
    }
    
    investment_unit = {
        'unit_id': 'INV-PACK-001',
        'type': 'Investment Package (5 Units)',
        'project': 'Rental Complex Pro',
        'price': '15,000,000 EGP',
        'unit_availability': 'Investment Opportunity - Limited Time'
    }
    
    print("Step 1: Notify management groups...")
    try:
        management_result = whatsapp.send_message(
            customer_info=investment_customer,
            unit_info=investment_unit,
            recipients=[os.getenv("WHATSAPP_GROUP_ID")],
            message_type="group"
        )
        print(f"Management notification: {management_result['statistics']['success_rate']}% success")
    except Exception as e:
        print(f"Management notification failed: {e}")
    
    print("Step 2: Alert senior sales agents...")
    try:
        agents_result = whatsapp.send_message(
            customer_info=investment_customer,
            unit_info=investment_unit,
            recipients=["+201129563904", "+201003869531"],
            message_type="individual"
        )
        print(f"Agent alerts: {agents_result['statistics']['success_rate']}% success")
    except Exception as e:
        print(f"Agent alerts failed: {e}")
    
    print("Workflow completed!")


def validation_example():
    """Example showing input validation."""
    print("=== Validation Example ===")
    
    whatsapp = WhatsAppMessenger(delay=2)
    
    customer_info = {
        'name': 'Validation Test',
        'phone': '+201000000000',
        'chat_summary': 'Testing validation features'
    }
    
    unit_info = {
        'unit_id': 'VAL-001',
        'type': 'Validation Unit',
        'project': 'Validation Project',
        'price': '1,000,000 EGP',
        'unit_availability': 'For Testing'
    }
    
    # Test invalid message type
    try:
        whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=["+201129563904"],
            message_type="invalid_type"
        )
    except ValidationError as e:
        print(f"✅ Caught invalid message type: {e}")
    
    # Test empty recipients
    try:
        whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=[],
            message_type="individual"
        )
    except ValidationError as e:
        print(f"✅ Caught empty recipients: {e}")
    
    # Test valid input
    try:
        result = whatsapp.send_message(
            customer_info=customer_info,
            unit_info=unit_info,
            recipients=["+201129563904"],
            message_type="individual"
        )
        print(f"✅ Valid input processed: {result['statistics']['success_rate']}% success")
    except Exception as e:
        print(f"❌ Unexpected error with valid input: {e}")


if __name__ == "__main__":
    examples = [
        single_group_example,
        single_individual_example,
        multiple_groups_example,
        multiple_individuals_example,
        error_handling_example,
        workflow_example,
        validation_example
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
            if i < len(examples):
                print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"Example {i} failed: {e}")
            if i < len(examples):
                print("\n" + "="*60 + "\n")