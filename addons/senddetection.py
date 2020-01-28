import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime 

sender = "mjkleben@gmail.com"
receiver = "mjkleben@gmail.com"
msg = MIMEMultipart('related')
msg['Subject'] = 	"Intruder: " + datetime.now().strftime("%a, %d %B %Y %I:%M:%S")
msg['From'] = sender
msg['To'] = receiver

html = """
<html>
  <head></head>
    <body>
      <img src="cid:image1" style="width:50vw;height:auto;"><br>
      <img src="cid:image2" style="width:50vw;height:auto;"><br>
    </body>
</html>
"""
# Record the MIME types of text/html.
part2 = MIMEText(html, 'html')

# Attach parts into message container.
msg.attach(part2)

# This example assumes the image is in the current directory
fp = open('detected.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

fp2 = open('detected2.jpg', 'rb')
msgImage2 = MIMEImage(fp2.read())
fp2.close()
msgImage.add_header('Content-ID', '<image2>')
msg.attach(msgImage2)

# Send the message via local SMTP server.
mailsrv = smtplib.SMTP('smtp.gmail.com:587')
mailsrv.ehlo()
mailsrv.starttls()
mailsrv.login(sender, "Iamthewinner123")

mailsrv.sendmail(sender, receiver, msg.as_string())
mailsrv.quit()
print("SENT")