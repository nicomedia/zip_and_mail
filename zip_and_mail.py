import sys
import os
import zipfile
import smtplib
import shutil
import os.path, time
from shutil import copyfile
from os.path import basename

# Python 3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# Python 2
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEBase import MIMEBase

base_folder     = PATH_FOR_BASE_FOLDER
copyto          = COPY_TO_EXTERNAL_HDD
fromaddr        = MAIL_ADDR_FROM
toaddr          = MAIL_ADDR_TO
password        = MAIL_PASSWORD

# MFO #
# Zip the folder --> send e-mail and copy to external storage
if __name__ == "__main__":
    # Find today's folder and archive
    datestring = datetime.strftime(datetime.now(), '%Y_%m_%d')
    newpath = base_folder + "mfo_" + datestring
    if os.path.exists(newpath):
        shutil.make_archive(newpath, 'zip', newpath)

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE EMAIL"
    body = "TEXT YOU WANT TO SEND"

###################### SEND E-MAIL ################################
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(newpath + ".zip", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(newpath + ".zip"))
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

###################### COPY TO STORAGE ################################
    if os.path.exists(copyto):
        copyfile(newpath + ".zip", copyto)
#        os.remove(newpath + ".zip")
#        os.remove(newpath)

