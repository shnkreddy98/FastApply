from validate_email import validate_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_PASS = os.getenv("sr20")

class emailRecipients:
    def __init__():
        pass

    def get_possible_emails(full_name, company, domain):
        if domain=="":
            domain = 'com'

        fn = full_name.lower().split(" ")[0]
        ln = full_name.lower().split(" ")[1]

        ffn = fn[0]
        fln = ln[0]

        symbs = [".", "-", "_"]

        possible_emails = [ln+fn, fln+fn, ln+ffn, 
                        fn+ln, ffn+ln, fn+fln]

        for symb in symbs:
            possible_emails.extend([fn+symb+ln, ffn+symb+ln, 
                                fn+symb+fln, ln+symb+fn, 
                                fln+symb+fn, ln+symb+ffn])
                            

        for i, email in enumerate(possible_emails):
            possible_emails[i] = f"{email}@{company}.{domain}"

        return possible_emails
    
    def get_valid_emails(possible_emails, from_addr):
        valid_emails = []
        for email in possible_emails:
            is_valid = validate_email(email_address=email,
                                      smtp_from_address=from_addr)
            if is_valid:
                valid_emails.append(email)

        return ['shashank.grad22@gmail.com']
    
    def send_emails(from_email, possible_emails, subject, body, resumefilepath):
        sent = 0
        for toaddr in possible_emails:
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = toaddr
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            filename = os.path.basename(resumefilepath)
            file_path = resumefilepath

            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={filename}")
                msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_email, EMAIL_PASS)
                text = msg.as_string()
                server.sendmail(from_email, toaddr, text)
                sent = 1
            except Exception as e:
                sent = 0
            finally:
                server.quit()

        return sent



