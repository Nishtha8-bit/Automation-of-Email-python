import imaplib
#import io
import email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

def send_email(send_email,send_pass,receiver):
    sender_email = send_email
    receiver_email = receiver
    password = send_pass
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reply"
    message["From"] = sender_email
    message["To"] = receiver_email

# Create the plain-text and HTML version of your message
    text = """\
        Hi,I have succesfully received your email
        """
    html = """\
                <html>
                <body>
                <p>Hi,<br>
                I have succesfully received your email
                </p>
                </body>
                </html>
                """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
            )



def send_email1():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    (retcode, capabilities) = mail.login('email_id','password')
    mail.list()
    mail.select('inbox')
    
    n=0
    retcode, messages = mail.search(None, '(UNSEEN)')
    if retcode == 'OK':
    
       for num in messages[0].split() :
          print ('Processing ')
          n=n+1
          
          typ, data = mail.fetch(num,'(RFC822)')
          for response in data:
             if isinstance(response, tuple):
                 original = email.message_from_string(response[1].decode('utf-8'))
    
                 print("From:" ,original['From'])
                 print("Subject:", original['Subject'])
                 typ, data = mail.store(num,'+FLAGS','\\Seen')
                 send_email('email_id','password', original['From'])
                 
    
    print(f"there is {n} messages")
#send_email1()
schedule.every(15).minute.do(send_email1)
while True:
    schedule.run_pending()
    time.sleep(1)
