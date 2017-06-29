#! /usr/local/bin/python
import sys
import os
import re
import csv

from smtplib import SMTP_SSL as SMTP   
from email.mime.text import MIMEText

USERNAME = "softlang"
PASSWORD = ""
destinationNameSender = "/Users/freddy/Desktop/NameEmail.csv"


SMTPserver = 'smtp.uni-koblenz.de:465'
sender =     'softlang@uni-koblenz.de'

# typical values for text_subtype are plain, html, xml
text_subtype = 'html'

template="""\
Dear [Developer], <br><br>

we, the Softlang research group of the University of Koblenz, would like to remind you about our survey related to
API usage in the Elasticsearch project. 
The survey is open till next week Friday and we need your participation for a successfull research:
<br>
<br>
<a href="https://www.soscisurvey.de/softlang/">https://www.soscisurvey.de/softlang/</a> - takes about 5 minutes
<br>
<br>
If you don't want to participate in the survey you would really help us if you shortly response to
this email and explain why and how we could improve.
<br>
<br>
Best regards and thanks in advance<br>
Ralf Laemmel and the Softlang team<br>
---<br>
http://www.softlang.org/

"""

subject="[Elasticsearch API survey] - Reminder and feedback"

def read_csv():
    with open(destinationNameSender, mode='rU') as infile:
        reader = csv.reader(infile, delimiter=";")
        emailName = {rows[0]:rows[1] for rows in reader}
    return emailName

        

try:
    print "Trying to connect"
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    print "Connected now reading the csv file " + destinationNameSender
    emailName = read_csv()
    print "Trying to send E-Mails"

    for email, name in emailName.iteritems():
        print "Sending mail to " + email + " with name " + name
        content = template.replace("[Developer]", name)
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        msg['cc'] = "softlang@uni-koblenz.de"
        msg['To']   = email
        
        conn.sendmail(sender, email, msg.as_string())
        
            
    conn.quit()
except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
