import smtplib, os, re
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = os.getenv("FILE_PATH", "output/orders.csv")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "a0988282303@gmail.com")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def is_valid_email(email: str):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def dump_and_email():
    df = pd.read_csv(FILE_PATH)
    content = pd.DataFrame(columns=["name", "address", "email", "items"])
    
    # Connect to the SMTP server (for Gmail, use smtp.gmail.com)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    
    subject = "Thank You for Your Recent Purchase at Lon's Shop"
    
    # email all customers
    for email in df['email'].unique():
        items = df.where(df['email'] == email).dropna()
        name = items['name'].values[0]
        address = items['address'].values[0]
        message = f"Dear {name},\n\nI wanted to take a moment to express my sincere gratitude for your recent purchase from Lon's Shop.\n\nHere's a summary of the items you purchased:\n"
        items_list = ""
        for i, c in zip(items['item_name'], items['count']):
            item = f"{i}x{int(c)}"
            items_list += f"{item} "
            message += f"{item}\n"
        
        message += "\nThank you once again for your trust in our company. If you have any feedback or suggestions for us, please feel free to share them." 
        message += "We are always looking for ways to improve and better serve our customers.\n\nWarm regards,\nJenny Lin\nLon's Shop"
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        if is_valid_email(email):
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
        
        order_result = {
            "name": name,
            "address": address,
            "email": email,
            "items": [items_list]
        }
        
        new_content = pd.DataFrame(data=order_result)
        content = pd.concat([content, new_content])
        
    server.quit()
    content.to_csv("output/order_result.csv", encoding='utf-8', index=False)
