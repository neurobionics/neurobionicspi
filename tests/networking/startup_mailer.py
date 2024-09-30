import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
from email.message import EmailMessage
import datetime
import os
import secrets
import time
import sys

def initialize_smtp(gmail_user, gmail_password):
    """
    Initializes an SMTP server with the provided login credentials.

    Parameters:
    -----------
    gmail_user: Email address of the mailer
    gmail_password: Passphrase for mailer's email

    Returns: smtlib.SMTP()
    """
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_password)

    return smtpserver

def get_ssid():
    """
    Retrieves the SSID of the current network.

    Returns: str
    """
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        ssid = "Could not get SSID"
    return ssid


def compose_email(gmail_user, recipients, ipaddr, mac, token, today, hostname, ssid):
    """
    Composes an e-mail with html formatting.

    Parameters:
    -----------
    gmail_user: Email address of mailer
    recipients: Email address(es) of recipient(s)
    ipaddr: IP Address of the device
    mac: MAC Address of the device
    token: Unique token generated for each session
    today: datetime formatted present date and time.

    Returns: EmailMessage()
    """
    msg = EmailMessage()
    msg['Subject'] = 'Session created for RPi @%s' % ipaddr
    msg['From'] = gmail_user
    msg['To'] = ",".join(str(x) for x in recipients)
    msg.set_content('''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html dir="ltr" lang="en">
        <head>
            <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        </head>

        <body style="background-color:rgb(0,0,0);margin-top:auto;margin-bottom:auto;margin-left:auto;margin-right:auto;font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;padding:1rem">
            <table align="center" width="100%" border="0" cellPadding="0" cellSpacing="0" role="presentation" style="max-width:700px;border-width:1px;border-style:solid;border-color:rgb(82, 82, 91);border-radius:0.375rem;margin-top:40px;margin-bottom:40px;margin-left:auto;margin-right:auto;padding:20px">
                <tbody>
                    <tr style="width:100%">
                        <td>
                            <h1 class="" style="font-weight:400;text-align:center;border-radius:0.375rem;padding:1rem;margin-bottom:12px;margin-left:0px;margin-right:0px;border-width:1px;border-style:solid;border-color:rgb(82, 82, 91)">
                                <p style="font-size:14px;line-height:28px;margin:16px 0;color:rgb(205, 205, 205);text-align:center;margin-bottom:12px"><strong style="color:rgb(255, 255, 255);font-size:32px">neurobionicspi</strong><br />IP Address Emailer Utility v3.0</p>
                            </h1>
                            <table align="center" width="100%" border="1" cellPadding="0" cellSpacing="0" role="presentation" style="border-radius:0.375rem;padding:1rem;margin-left:auto;margin-right:auto;border-width:1px;border-style:solid;border-color:rgb(82, 82, 91)">
                                <tbody align="center" width="100%" style="color:rgb(255,255,255);">
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">Hostname:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{5}</td>
                                    </tr>                                   
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">IP Address:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;"><strong style="color:rgb(165,243,252)">{0}</strong></td>
                                    </tr>
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">MAC Address:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{2}</td>
                                    </tr>                                    
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">From Network:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{6}</td>
                                    </tr>
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">Unique Identifier:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{1}</td>
                                    </tr>
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">Date:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{3}</td>
                                    </tr>
                                    <tr style="border: 1px solid rgb(38, 38, 38);">
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">Time:</td>
                                        <td style="border: 1px solid rgb(38, 38, 38); text-align: left; padding: 10px;">{4}</td>
                                    </tr>
                                </tbody>
                            </table>
                            <h1 class="" style="font-weight:400;text-align:center;border-radius:0.375rem;padding:1rem;margin-bottom:12px;margin-left:0px;margin-right:0px;border-width:1px;border-style:solid;border-color:rgb(82, 82, 91)">
                                <img alt="Michigan Robotics" height="auto" src="https://neurobionics.robotics.umich.edu/wp-content/themes/wp-tailwind-light-robotics-lab-child/mrobotics-reverse.png" style="display:block;outline:none;border:none;text-decoration:none;margin-left:auto;margin-right:auto;margin-top:12px" width="230"/>
                                <p style="font-size:10px;line-height:12px;margin:16px 0;color:rgb(163, 163, 163)" align="center">© 2024 Neurobionics Lab, University of Michigan <br /></p>
                            </h1>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    '''.format(ipaddr, token, mac, today.strftime('%d %b %Y'), today.strftime('%I:%M:%S %p'), hostname, ssid), subtype='html')
    return msg

def send_email(smtpserver, msg):
    """
    Sends an email

    Parameters:
    -----------
    smtpserver: smtlib.SMTP()
    msg: EmailMessage()

    """
    smtpserver.send_message(msg)
    smtpserver.quit()

if __name__ == '__main__':

    # Modify recipients here!
    recipient_str = "senthura@umich.edu"
    recipients = recipient_str.split(", ")

    #######################################################

    # Initializing an SMTP server with mailer credentials

    gmail_user = 'neurobionics-rpi-emailer@umich.edu'
    gmail_password = 'oIxS7gniIEDejPwa'

    try:
        smtpserver = initialize_smtp(gmail_user, gmail_password)

        #######################################################

        # Retrieving information from the host

        utctoday = datetime.datetime.utcnow() #UTC
        utc2est = datetime.timedelta(hours=5)
        today = utctoday - utc2est #EST

        hostname = socket.gethostname()
        ssid = get_ssid()

        # Get MAC address - individual ID for each device
        str_temp = open('/sys/class/net/wlan0/address').read()
        mac = str_temp[0:17]

        arg = 'ip route list'
        p = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()
        temp = str(data[0])
        split_data = temp.split()
        ipaddr = split_data[split_data.index('src')+1]

        #Generates an unique token for each session
        token = secrets.token_urlsafe(16)

        #######################################################

        # Compose and send an e-mail
        msg = compose_email(gmail_user, recipients, ipaddr, mac, token, today, hostname, ssid)
        send_email(smtpserver, msg)

        print("A ticket for the current session has been mailed to the recipient(s).")
        sys.exit(0) # Success

    except Exception as e:
        print("Mailer script failed:", str(e))
        sys.exit(1)  # Exit with failure status
