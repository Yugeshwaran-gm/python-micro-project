import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, config=None):
        self.config = config
        
    def send_email(self, recipient, subject, body):
        if not self.config:
            print("No config provided")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = self.config['MAIL_USERNAME']
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        try:
            server = smtplib.SMTP(self.config['MAIL_SERVER'], self.config['MAIL_PORT'])
            server.starttls()
            server.login(self.config['MAIL_USERNAME'], self.config['MAIL_PASSWORD'])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
