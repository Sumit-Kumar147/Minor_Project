# test_email.py
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_configuration():
    # Load environment variables
    load_dotenv()
    
    # Get email configuration
    sender_email = os.getenv("FROM_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("TO_EMAIL")
    
    # Print configuration (without password)
    print(f"Sender: {sender_email}")
    print(f"Receiver: {receiver_email}")
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Test Email from Garbage Detection System"
        
        # Add body
        body = """
        This is a test email from your Garbage Detection System.
        If you receive this, your email configuration is working correctly.
        """
        message.attach(MIMEText(body, "plain"))
        
        # Create SMTP session
        print("Connecting to SMTP server...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("Attempting login...")
            server.login(sender_email, password)
            print("Login successful")
            
            # Send email
            print("Sending test email...")
            server.send_message(message)
            print("Test email sent successfully!")
            
        return True
    except Exception as e:
        print(f"Error sending test email: {str(e)}")
        return False

if __name__ == "__main__":
    test_email_configuration()