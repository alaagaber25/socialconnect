"""Email templates for various message types."""

from typing import Dict
from datetime import datetime


class EmailTemplates:
    """Container for email template methods."""
    
    def create_client_inquiry_html(self, client_data: Dict, inquiry_time: str) -> str:
        """Creates an HTML formatted email body for client inquiry."""
        unit_details = client_data.get('unit_details', {})
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #2c5aa0;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border: 1px solid #ddd;
                }}
                .section {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: white;
                    border-radius: 5px;
                    border-left: 4px solid #2c5aa0;
                }}
                .section h3 {{
                    margin-top: 0;
                    color: #2c5aa0;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 5px;
                }}
                .info-row {{
                    margin: 8px 0;
                }}
                .label {{
                    font-weight: bold;
                    color: #555;
                    display: inline-block;
                    width: 120px;
                }}
                .value {{
                    color: #333;
                }}
                .footer {{
                    background-color: #f0f0f0;
                    padding: 15px;
                    text-align: center;
                    border-radius: 0 0 8px 8px;
                    font-size: 12px;
                    color: #666;
                }}
                .urgent {{
                    background-color: #fff3cd;
                    border-left-color: #ffc107;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏠 New Client Inquiry</h1>
                <p>Property Interest Notification</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h3>👤 Client Information</h3>
                    <div class="info-row">
                        <span class="label">Name:</span>
                        <span class="value">{client_data.get('client_name', 'Not provided')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Phone:</span>
                        <span class="value">{client_data.get('phone_number', 'Not provided')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Inquiry Time:</span>
                        <span class="value">{inquiry_time}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>🏢 Unit Details</h3>
                    <div class="info-row">
                        <span class="label">Project:</span>
                        <span class="value">{unit_details.get('project_name', 'Not specified')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Unit Type:</span>
                        <span class="value">{unit_details.get('unit_type', 'Not specified')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Unit Number:</span>
                        <span class="value">{unit_details.get('unit_number', 'Not specified')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Size:</span>
                        <span class="value">{unit_details.get('size', 'Not specified')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Price:</span>
                        <span class="value">{unit_details.get('price', 'Not specified')}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Floor:</span>
                        <span class="value">{unit_details.get('floor', 'Not specified')}</span>
                    </div>
                </div>
                
                <div class="section">
                    <h3>💬 Chat Description</h3>
                    <p style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 0;">
                        {client_data.get('chat_description', 'No chat description provided')}
                    </p>
                </div>
                
                <div class="section urgent">
                    <h3>📋 Client Request/Needs</h3>
                    <p style="background-color: #fff; padding: 10px; border-radius: 4px; margin: 0;">
                        {client_data.get('client_request', 'No specific request mentioned')}
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>This is an automated notification from your property inquiry system.</p>
                <p>Please follow up with the client promptly for the best service experience.</p>
            </div>
        </body>
        </html>
        """
        return html_template

    def create_client_inquiry_text(self, client_data: Dict, inquiry_time: str) -> str:
        """Creates a plain text version of the client inquiry email."""
        unit_details = client_data.get('unit_details', {})
        
        text_body = f"""
NEW CLIENT INQUIRY - PROPERTY INTEREST
=====================================

CLIENT INFORMATION:
------------------
Name: {client_data.get('client_name', 'Not provided')}
Phone: {client_data.get('phone_number', 'Not provided')}
Inquiry Time: {inquiry_time}

UNIT DETAILS:
------------
Project: {unit_details.get('project_name', 'Not specified')}
Unit Type: {unit_details.get('unit_type', 'Not specified')}
Unit Number: {unit_details.get('unit_number', 'Not specified')}
Size: {unit_details.get('size', 'Not specified')}
Price: {unit_details.get('price', 'Not specified')}
Floor: {unit_details.get('floor', 'Not specified')}

CHAT DESCRIPTION:
----------------
{client_data.get('chat_description', 'No chat description provided')}

CLIENT REQUEST/NEEDS:
--------------------
{client_data.get('client_request', 'No specific request mentioned')}

=====================================
This is an automated notification from your property inquiry system.
Please follow up with the client promptly for the best service experience.
"""
        return text_body