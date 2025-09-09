# SocialConnect

A comprehensive Python library for automating messaging across email and WhatsApp platforms. Designed specifically for real estate sales teams, customer service departments, and automated notification systems. Send professional client inquiry emails and WhatsApp messages with rich formatting and comprehensive error handling.

## ✨ Features

- **📧 Email Messaging**: Send beautifully formatted HTML emails with professional client inquiry templates
- **📱 WhatsApp Messaging**: Automated WhatsApp messaging to individuals and groups with rich formatting
- **⚙️ Flexible Configuration**: Environment variables, programmatic setup, or custom configurations
- **🛡️ Error Handling**: Comprehensive error handling with detailed logging and statistics
- **🔧 Extensible Design**: Easy to extend with new messaging platforms
- **📝 Type Safety**: Full type annotation support for better development experience
- **🎯 Sales-Focused**: Pre-built templates for real estate and sales use cases

## 🚀 Installation

```bash
pip install socialconnect
```

Or install from source:
```bash
git clone https://github.com/alaagaber25/socialconnect.git
cd socialconnect
pip install -e .
```

## 📖 Quick Start

### 📧 Email Messaging

Send professional client inquiry emails with rich HTML templates:

```python
from socialconnect import EmailMessenger

# Initialize with credentials (or use environment variables)
email_messenger = EmailMessenger("your-email@gmail.com", "your-app-password")

# Or use environment variables (GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
email_messenger = EmailMessenger()

# Prepare client data with detailed information
client_data = {
    'client_name': 'Ahmed Hassan',
    'phone_number': '+20 12 3456 7890',
    'chat_description': 'Client contacted via WhatsApp expressing interest in a 2-bedroom apartment with garden view.',
    'unit_details': {
        'project_name': 'New Capital Heights',
        'unit_type': '2-Bedroom Apartment', 
        'unit_number': 'A-205',
        'size': '120 sqm',
        'price': '2,800,000 EGP',
        'floor': '2nd Floor'
    },
    'inquiry_time': '2024-12-15 14:30:00',
    'client_request': 'Interested in flexible payment plan and wants to schedule a site visit next weekend.'
}

# Send to single or multiple recipients
result = email_messenger.send_message(
    client_data=client_data,
    email_addresses=["agent@company.com", "manager@company.com"]
)

print(f"✅ Success rate: {result['statistics']['success_rate']}%")
print(f"📧 Emails sent: {result['statistics']['successful']}/{result['statistics']['total_sent']}")
```

### 📱 WhatsApp Messaging

Send formatted messages to WhatsApp groups or individuals:

```python
from socialconnect import WhatsAppMessenger

# Initialize messenger with custom delay
whatsapp_messenger = WhatsAppMessenger(delay=5, close_tab=True)

# Prepare customer and unit information
customer_info = {
    'name': 'Sarah Mohamed',
    'phone': '+201234567890',
    'chat_summary': 'Looking for luxury apartment near metro station, budget up to 3M EGP'
}

unit_info = {
    'unit_id': 'LUX-001',
    'type': 'Penthouse',
    'project': 'Luxury Heights',
    'price': '2,800,000 EGP',
    'unit_availability': 'Available - Last Unit!'
}

# Send to WhatsApp group
group_result = whatsapp_messenger.send_message(
    customer_info=customer_info,
    unit_info=unit_info,
    recipients="YOUR_GROUP_ID",
    message_type="group"
)

# Send to multiple individuals
individual_result = whatsapp_messenger.send_message(
    customer_info=customer_info,
    unit_info=unit_info,
    recipients=["+201111111111", "+201222222222", "+201333333333"],
    message_type="individual"
)

print(f"📱 Group message success rate: {group_result['statistics']['success_rate']}%")
print(f"👥 Individual messages success rate: {individual_result['statistics']['success_rate']}%")
```

## ⚙️ Configuration

### 🌍 Environment Variables

The recommended way to configure SocialConnect is using environment variables. Create a `.env` file in your project root:

```env
# Email Configuration (Required)
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-specific-password

# SMTP Configuration (Optional - defaults to Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# WhatsApp Configuration (Optional)
WHATSAPP_DELAY=5
WHATSAPP_GROUP_ID=your-default-group-id
```

> **⚠️ Security Note**: Never commit your `.env` file to version control. Add it to your `.gitignore`.

### 🛠️ Programmatic Configuration

You can also configure settings programmatically:

```python
from socialconnect.config import SocialConnectConfig

# Initialize configuration
config = SocialConnectConfig()

# Update email settings
config.update_email_config(
    sender_email="sales@company.com",
    smtp_server="smtp.company.com",
    smtp_port=587
)

# Update WhatsApp settings  
config.update_whatsapp_config(delay=3, close_tab=False)

# View current configuration
print(config.to_dict())
```

### 🔐 Gmail App Password Setup

For Gmail users, you need to generate an App Password:

1. Enable 2-Step Verification on your Google Account
2. Go to Google Account Settings → Security → 2-Step Verification
3. Scroll down and select "App passwords"
4. Generate an app password for "Mail"
5. Use this 16-character password in your configuration

## 🔥 Advanced Usage

### 🛡️ Error Handling & Validation

SocialConnect provides comprehensive error handling with custom exceptions:

```python
from socialconnect import EmailMessenger, WhatsAppMessenger
from socialconnect.core.exceptions import (
    SocialConnectError, 
    AuthenticationError, 
    ValidationError,
    MessagingError
)

# Email error handling
try:
    messenger = EmailMessenger()
    result = messenger.send_message(client_data, emails)
    
    # Check individual results
    for email, details in result['results'].items():
        if not details['success']:
            print(f"❌ Failed to send to {email}: {details['error']}")
            
except AuthenticationError as e:
    print(f"🔐 Authentication failed: {e}")
except ValidationError as e:
    print(f"⚠️ Validation error: {e}")
except SocialConnectError as e:
    print(f"💥 Messaging error: {e}")

# WhatsApp error handling with validation
try:
    whatsapp = WhatsAppMessenger(delay=3)
    
    # This will validate phone numbers automatically
    result = whatsapp.send_message(
        customer_info=customer_info,
        unit_info=unit_info, 
        recipients=["+201234567890", "invalid-phone"],  # Mix of valid/invalid
        message_type="individual"
    )
    
    # Review results
    for recipient, details in result['results'].items():
        status = "✅" if details['success'] else "❌"
        print(f"{status} {recipient}: {details.get('error', 'Success')}")
        
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### 📊 Batch Processing & Analytics

Process multiple clients efficiently with detailed analytics:

```python
from socialconnect import EmailMessenger
import time

email_messenger = EmailMessenger()

# Sample client database
clients_database = [
    {
        'client_name': 'Ahmed Hassan',
        'phone_number': '+201234567890',
        'chat_description': 'Interested in 2-bedroom apartment',
        'unit_details': {'project_name': 'Sunset Towers', 'price': '2.5M EGP'},
        'client_request': 'Wants viewing appointment'
    },
    # ... more clients
]

# Batch processing with progress tracking
results_summary = []
for i, client_data in enumerate(clients_database, 1):
    print(f"Processing client {i}/{len(clients_database)}: {client_data['client_name']}")
    
    result = email_messenger.send_message(
        client_data=client_data,
        email_addresses=[f"agent{i}@company.com", "manager@company.com"]
    )
    
    results_summary.append({
        'client': client_data['client_name'],
        'success_rate': result['statistics']['success_rate'],
        'emails_sent': result['statistics']['successful'],
        'timestamp': time.time()
    })
    
    # Rate limiting to avoid overwhelming the email server
    time.sleep(2)

# Overall analytics
total_emails = sum(r['emails_sent'] for r in results_summary)
avg_success_rate = sum(r['success_rate'] for r in results_summary) / len(results_summary)

print(f"\n📊 Batch Processing Summary:")
print(f"   Total clients processed: {len(results_summary)}")
print(f"   Total emails sent: {total_emails}")
print(f"   Average success rate: {avg_success_rate:.1f}%")
```

### 🎨 Custom Email Templates

Create your own email templates or modify existing ones:

```python
from socialconnect.email.templates import EmailTemplates
from datetime import datetime

# Use built-in templates
templates = EmailTemplates()

# Generate custom HTML email
client_data = {
    'client_name': 'Omar Khalil',
    'phone_number': '+201987654321',
    # ... other data
}

inquiry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
custom_html = templates.create_client_inquiry_html(client_data, inquiry_time)
custom_text = templates.create_client_inquiry_text(client_data, inquiry_time)

print("Generated HTML template length:", len(custom_html))
print("Generated text template length:", len(custom_text))
```

### 🔄 WhatsApp Workflow Automation

Implement complex WhatsApp workflows for different scenarios:

```python
from socialconnect import WhatsAppMessenger
import os

whatsapp = WhatsAppMessenger(delay=3, close_tab=True)

def handle_premium_client(customer_info, unit_info):
    """Handle high-value clients with escalated notifications."""
    
    # Step 1: Notify management immediately
    management_result = whatsapp.send_message(
        customer_info=customer_info,
        unit_info=unit_info,
        recipients=[os.getenv("MANAGEMENT_GROUP_ID")],
        message_type="group"
    )
    
    # Step 2: Alert senior sales team
    senior_agents = ["+201111111111", "+201222222222"]
    agents_result = whatsapp.send_message(
        customer_info=customer_info,
        unit_info=unit_info,
        recipients=senior_agents,
        message_type="individual"
    )
    
    return {
        'management_notified': management_result['statistics']['success_rate'] == 100,
        'agents_alerted': agents_result['statistics']['successful'],
        'total_notifications': (
            management_result['statistics']['successful'] + 
            agents_result['statistics']['successful']
        )
    }

# Usage example
premium_customer = {
    'name': 'High Value Client',
    'phone': '+201555666777',
    'chat_summary': 'Interested in multiple luxury units - Investment opportunity'
}

luxury_unit = {
    'unit_id': 'LUX-PENTHOUSE-001',
    'type': 'Penthouse Suite',
    'project': 'Elite Towers',
    'price': '8,000,000 EGP',
    'unit_availability': 'Exclusive - Last Unit'
}

workflow_result = handle_premium_client(premium_customer, luxury_unit)
print(f"🎯 Premium client workflow: {workflow_result}")
```

## 📋 Requirements

- **Python**: 3.13+ (recommended), minimum 3.8+
- **Dependencies**:
  - `pywhatkit>=5.4` - WhatsApp Web automation
  - `pyperclip>=1.8.2` - Clipboard operations
  - `pyautogui>=0.9.54` - GUI automation 
  - `python-dotenv>=1.0.0` - Environment variable management

### 🖥️ System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Internet Connection**: Required for WhatsApp Web and SMTP
- **Display**: Required for WhatsApp automation (uses browser automation)
- **Permissions**: Screen control permissions may be required for WhatsApp automation

### 🌐 Browser Support

WhatsApp messaging requires a web browser (Chrome recommended) and WhatsApp Web access.

## 🔧 Development

### 🏗️ Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/alaagaber25/socialconnect.git
cd socialconnect

# Install in development mode with dependencies
pip install -e .

# Install additional development dependencies (if available)
pip install pytest black flake8 mypy

# Set up your environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 🧪 Running Examples

The project includes comprehensive examples in the `examples/` directory:

```bash
# Basic usage examples
python examples/basic_usage.py

# Advanced WhatsApp workflows  
python examples/advanced_usage.py

# Configuration examples
python examples/config_examples.py
```

### 🧹 Code Quality

```bash
# Format code with Black
black socialconnect/

# Check code style with Flake8
flake8 socialconnect/

# Type checking with MyPy
mypy socialconnect/
```

### 📁 Project Structure

```
socialconnect/
├── socialconnect/           # Main package
│   ├── core/               # Base classes and exceptions
│   ├── email/              # Email messaging module
│   ├── whatsapp/           # WhatsApp messaging module
│   ├── utils/              # Utility functions
│   └── config/             # Configuration management
├── examples/               # Usage examples
└── docs/                   # Documentation (if available)
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 🌟 How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with clear, documented code
4. **Add tests** for new functionality
5. **Ensure code quality**: Run `black` and `flake8`
6. **Commit your changes**: `git commit -m "Add amazing feature"`
7. **Push to your branch**: `git push origin feature/amazing-feature`
8. **Submit a Pull Request**

### 🎯 Areas for Contribution

- 📱 Additional messaging platforms (Telegram, Discord, Slack)
- 🎨 More email templates and customization options
- 🧪 Comprehensive test suite
- 📚 Documentation improvements
- 🐛 Bug fixes and performance improvements
- 🌍 Internationalization support

### 📝 Contribution Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where possible
- Update examples if adding new features
- Add appropriate error handling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🔓 MIT License Summary

- ✅ Commercial use allowed
- ✅ Modification allowed  
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability accepted

## 🆘 Support & Community

### 🐛 Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/alaagaber25/socialconnect/issues)
- **Discussions**: [Join community discussions](https://github.com/alaagaber25/socialconnect/discussions)
- **Email**: [alaagaber25@gmail.com](mailto:alaagaber25@gmail.com)

### 📊 Project Stats

- 🌟 **Version**: 0.1.0
- 🐍 **Python**: 3.13+
- 📦 **Dependencies**: 4 core packages
- 🏗️ **Architecture**: Modular, extensible design
- 🧪 **Status**: Active development

## 🚀 Roadmap & Changelog

### 🎯 Upcoming Features (v0.2.0)

- [ ] 📊 Built-in analytics dashboard
- [ ] 🔄 Message scheduling and automation
- [ ] 📱 Telegram support
- [ ] 🎨 More email template themes
- [ ] 🧪 Comprehensive test coverage
- [ ] 📖 Complete API documentation

### 📅 Version History

#### v0.1.0 (Current)
- 🎉 Initial release
- 📧 Email messaging with HTML templates
- 📱 WhatsApp messaging for individuals and groups
- ⚙️ Comprehensive configuration system
- 🛡️ Error handling and validation
- 📝 Usage examples and documentation
- 🏗️ Modular architecture with extensibility

---

## 🌟 Star History

If you find SocialConnect useful, please consider giving it a star ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=alaagaber25/socialconnect&type=Date)](https://star-history.com/#alaagaber25/socialconnect&Date)

---

## 📋 Quick Reference

### 💡 Environment Variables Template

Create a `.env` file in your project root:

```env
# 📧 Email Configuration (Required)
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password

# 🌐 SMTP Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# 📱 WhatsApp Configuration (Optional)
WHATSAPP_DELAY=5
WHATSAPP_GROUP_ID=your-default-group-id
```

### 🔗 Quick Links

- 📖 **Documentation**: [GitHub Repository](https://github.com/alaagaber25/socialconnect)
- 💻 **Examples**: Check the `examples/` directory
- 🐛 **Issues**: [Report Problems](https://github.com/alaagaber25/socialconnect/issues)
- 💡 **Discussions**: [Community](https://github.com/alaagaber25/socialconnect/discussions)

### 📞 Contact Information

- 👨‍💻 **Developer**: Alaa Gaber
- 📧 **Email**: [alaagaber25@gmail.com](mailto:alaagaber25@gmail.com)
- 🐙 **GitHub**: [@alaagaber25](https://github.com/alaagaber25)

---

<div align="center">

**Made with ❤️ for the sales and real estate community**

[⭐ Star this repository](https://github.com/alaagaber25/socialconnect) • [🐛 Report Bug](https://github.com/alaagaber25/socialconnect/issues) • [💡 Request Feature](https://github.com/alaagaber25/socialconnect/issues)

</div>