#-------------------------------------------------------------------------------
# Name:        Sending reports using Estfeed report address
# Purpose:
#
# Author:      kristjan.vilgo
#
# Created:     14.11.2017
# Copyright:   (c) kristjan.vilgo 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import smtplib
import os
import datetime
import getpass
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

def send_report_email(subject, message, to_list, files_list):
    """Sends email trough SMTP account
        subject -> string
        message -> string
        to_list -> list string of email rescipients addresses
        files_list -> list of full path strings to files to be attached
    """



    # SMTP account settings

    with open("smtp_config.json", "r") as smtp_config_file:
        smtp_config = json.load(smtp_config_file)
        print smtp_config

##    smtp_config = {
##    "host":"smtp.gmail.com",
##    "port" : 587,
##    "username" : "",
##    "password" : ""
##    }




    # SMTP setup
    smtp = smtplib.SMTP(host = smtp_config["host"], port = smtp_config["port"])
    smtp.starttls()
    smtp.login(smtp_config["username"], smtp_config["password"])

    # form e-mail
    datetime_now = datetime.datetime.now()
    email = MIMEMultipart()
    email["From"] = smtp_config["username"]
    email["To"]   = ", ".join(to_list)
    email["Subject"] = "REPORT [{}] {:%d-%m-%YT%H:%M}".format(subject, datetime_now)

    email.attach(MIMEText("{} \n \n [Automated message] \n User: {} \n Timestamp: {}".format(message, getpass.getuser(), datetime_now),'plain','utf-8'))

    # add Attcahments
    for file in files_list:

        if os.path.exists(file) == True:

            attachment = MIMEBase('application', "octet-stream")
            attachment.set_payload(open(file, "rb").read())
            Encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(file)))
            email.attach(attachment)

        else:
            print "File not found and will not be attached {}".format(file)

    # send message and close SMPT connection
    smtp.sendmail(smtp_config["username"], to_list, email.as_string())
    smtp.quit()


# TEST
if __name__ == '__main__':
    send_report_email("Subject goes here", "Message goes here", ["kristjan.vilgo@elering.ee"],[])
