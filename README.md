# SocialConnect

A comprehensive Python library for sending messages across various social media and messaging platforms including email and WhatsApp. Perfect for sales teams, customer service, and automated notifications.

## Features

- **Email Messaging**: Send beautifully formatted HTML emails with client inquiry templates
- **WhatsApp Messaging**: Send messages to individuals or groups with automated formatting
- **Flexible Configuration**: Environment variables, programmatic setup, or custom configurations
- **Error Handling**: Comprehensive error handling with detailed logging
- **Extensible Design**: Easy to extend with new messaging platforms
- **Type Hints**: Full type annotation support
- **Testing**: Complete test suite included

## Installation

```bash
pip install socialconnect
```

## Quick Start

### Email Messaging

```python
from socialconnect import EmailMessenger

# Initialize with credentials
email_messenger = EmailMessenger("your-email@gmail.com", "your-app-password")

# Or use environment variables (GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
email_messenger = EmailMessenger()

# Send client inquiry email
client_data = {
    'client_name': 'John Doe',
    'phone_number': '+1234567890',
    'chat_description': 'Interested in 2-bedroom apartment',
    'unit_details': {
        'project_name': 'Sunset Towers',
        'unit_type': '2-Bedroom',
        'price': '$250,000'
    },
    'client_request': 'Wants to schedule viewing'
}

result = email_messenger.send_message(
    client_data=client_data,
    email_addresses=["agent@company.com", "manager@company.com"]
)

print(f"Success rate: {result['statistics']['success_rate']}%")
```

### WhatsApp Messaging

```python
from socialconnect import WhatsAppMessenger

# Initialize messenger
whatsapp_messenger = WhatsAppMessenger(delay=5)

# Prepare data
customer_info = {
    'name': 'Jane Smith',
    'phone': '+1234567890',
    'chat_summary': 'Looking for luxury apartment'
}

unit_info = {
    'unit_id': 'LUX-001',
    'type': 'Penthouse',
    'project': 'Luxury Heights',
    'price': '$500,000',
    'unit_availability': 'Available'
}

# Send to WhatsApp group
group_result = whatsapp_messenger.send_to_group(
    customer_info=customer_info,
    unit_info=unit_info,
    group_id="YOUR_GROUP_ID"
)

# Send to individuals
individual_result = whatsapp_messenger.send_to_individuals(
    customer_info=customer_info,
    unit_info=unit_info,
    phone_numbers=["+1111111111", "+2222222222"]
)
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
WHATSAPP_DELAY=5
```

### Programmatic Configuration

```python
from socialconnect.config import SocialConnectConfig

config = SocialConnectConfig()

# Update email settings
config.update_email_config(
    sender_email="custom@company.com",
    smtp_server="smtp.company.com"
)

# Update WhatsApp settings
config.update_whatsapp_config(delay=3)
```

## Advanced Usage

### Error Handling

```python
from socialconnect import EmailMessenger
from socialconnect.core.exceptions import SocialConnectError, AuthenticationError

try:
    messenger = EmailMessenger()
    result = messenger.send_message(client_data, emails)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except SocialConnectError as e:
    print(f"Messaging error: {e}")
```

### Batch Processing

```python
# Process multiple clients
clients = [client1_data, client2_data, client3_data]

for i, client_data in enumerate(clients):
    result = email_messenger.send_message(
        client_data=client_data,
        email_addresses=[f"agent{i+1}@company.com"]
    )
    print(f"Client {i+1}: {result['statistics']['success_rate']}% success")
```

### Custom Templates

```python
from socialconnect.email.templates import EmailTemplates

templates = EmailTemplates()
custom_html = templates.create_client_inquiry_html(client_data, inquiry_time)
```

## Requirements

- Python 3.7+
- pywhatkit>=5.4
- pyperclip>=1.8.2
- pyautogui>=0.9.54
- python-dotenv>=1.0.0

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/socialconnect.git
cd socialconnect
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black socialconnect/
flake8 socialconnect/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: [https://github.com/yourusername/socialconnect/issues]
- Email: support@socialconnect.dev

## Changelog

### v1.0.0
- Initial release
- Email messaging with HTML templates
- WhatsApp messaging for individuals and groups
- Comprehensive configuration system
- Full test coverage
- Documentation and examples

## .env (Template)
# Email Configuration
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password

# SMTP Configuration (optional, defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# WhatsApp Configuration (optional)
WHATSAPP_DELAY=5