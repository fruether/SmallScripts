#! /usr/local/bin/python
import sys
import os
import re
import csv

from smtplib import SMTP_SSL as SMTP   
from email.mime.text import MIMEText

USERNAME = "softlang"
PASSWORD = ""
destinationNameSender = "EmailDeveloper.csv"


SMTPserver = 'smtp.uni-koblenz.de:465'
sender =     'softlang@uni-koblenz.de'

# typical values for text_subtype are plain, html, xml
text_subtype = 'html'

template="""\
Dear [Name], <br>
<br>
I would like to kindly remind you about our developer survey on API usage in the Elasticsearch project. The survey is open till next week Friday. We appreciate your participation in the survey that helps our research on software development: <br><br>

<a href="https://www.soscisurvey.de/softlang/">https://www.soscisurvey.de/softlang/</a> - takes about 5 minutes <br><br>
If you don't want to participate in the survey, we would still appreciate your feedback, thereby possibly helping us with improving our surveying approach. To provide feedback outside the survey form, simply respond to this email.<br><br>

Thank you<br>
Ralf Laemmel for the Softlang team<br>
University of Koblenz-Landau<br>
Computer Science Faculty<br>
Germany<br>
<a href="http://www.softlang.org/">http://www.softlang.org/</a><br>
<a href="http://www.softlang.org/rlaemmel:home">http://www.softlang.org/rlaemmel:home</a>

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
        content = template.replace("[Name]", name)
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        msg['cc'] = "softlang@uni-koblenz.de"
        msg['To']   = email
        
        conn.sendmail(sender, email, msg.as_string())
        
            
    conn.quit()
except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
