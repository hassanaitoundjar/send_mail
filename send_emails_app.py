import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox
import configparser

# Load SMTP configuration from config.ini
def load_smtp_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'server': config['SMTP']['server'],
        'port': int(config['SMTP']['port']),
        'username': config['SMTP']['username'],
        'password': config['SMTP']['password'],
        'sender_email': config['EMAIL']['sender_email'],
        'subject': config['EMAIL']['subject']
    }

# Load email template from message_template.txt
def load_message_template():
    with open('message_template.txt', 'r') as file:
        return file.read()

# Function to send email
def send_email():
    try:
        # Load SMTP config and email template
        smtp_config = load_smtp_config()
        template = load_message_template()

        # Get customer details from the GUI
        name = name_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        dns = dns_entry.get()
        samsung_lg_dns = samsung_lg_dns_entry.get()
        m3u_url = m3u_url_entry.get()
        whatsapp_contact = whatsapp_contact_entry.get()

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = smtp_config['sender_email']
        msg['To'] = email
        msg['Subject'] = smtp_config['subject']

        # Personalize the email body
        body = template.format(
            name=name,
            username=username,
            password=password,
            dns=dns,
            samsung_lg_dns=samsung_lg_dns,
            m3u_url=m3u_url,
            whatsapp_contact=whatsapp_contact
        )
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.sendmail(smtp_config['sender_email'], email, msg.as_string())
        
        # Update status log
        status_log.insert(tk.END, f"Email sent to {email}\n")
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        status_log.insert(tk.END, f"Failed to send email: {e}\n")
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Create the main window
root = tk.Tk()
root.title("IPTV Email Sender")

# Customer Details Frame
customer_frame = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10)
customer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(customer_frame, text="Name:").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(customer_frame)
name_entry.grid(row=0, column=1)

tk.Label(customer_frame, text="Email:").grid(row=1, column=0, sticky="e")
email_entry = tk.Entry(customer_frame)
email_entry.grid(row=1, column=1)

tk.Label(customer_frame, text="Username:").grid(row=2, column=0, sticky="e")
username_entry = tk.Entry(customer_frame)
username_entry.grid(row=2, column=1)

tk.Label(customer_frame, text="Password:").grid(row=3, column=0, sticky="e")
password_entry = tk.Entry(customer_frame)
password_entry.grid(row=3, column=1)

tk.Label(customer_frame, text="DNS:").grid(row=4, column=0, sticky="e")
dns_entry = tk.Entry(customer_frame)
dns_entry.grid(row=4, column=1)

tk.Label(customer_frame, text="Samsung/LG DNS:").grid(row=5, column=0, sticky="e")
samsung_lg_dns_entry = tk.Entry(customer_frame)
samsung_lg_dns_entry.grid(row=5, column=1)

tk.Label(customer_frame, text="M3U URL:").grid(row=6, column=0, sticky="e")
m3u_url_entry = tk.Entry(customer_frame)
m3u_url_entry.grid(row=6, column=1)

tk.Label(customer_frame, text="WhatsApp Contact:").grid(row=7, column=0, sticky="e")
whatsapp_contact_entry = tk.Entry(customer_frame)
whatsapp_contact_entry.grid(row=7, column=1)

# Send Button
send_button = tk.Button(root, text="Send Email", command=send_email)
send_button.grid(row=1, column=0, pady=10)

# Status Log
status_log = tk.Text(root, height=10, width=60)
status_log.grid(row=2, column=0, padx=10, pady=10)

# Run the application
root.mainloop()
