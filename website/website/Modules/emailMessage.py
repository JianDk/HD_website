import smtplib
import email
import json
from threading import Thread

class sendEmail:
    def __init__(self, form, sourceFrom, emailTo):
        '''
        form is the django form. 
        
        SourceFrom is a string stating from which site the contact form was sent from. For example 'Hidden Dimsum 2900' indicating that the contact
        form was sent from Hidden Dimsum 2900.

        emailTo is the target mail address for which the content in django form should be sent to.
        '''
        
        #This email is sent to emailTo
        #Build the message body
        message = '''
        From %s
        Phone %s
        Email %s 

        Message
        %s
        ''' % (form.cleaned_data['senderName'], 
        form.cleaned_data['senderPhone'], 
        form.cleaned_data['senderEmail'],
        form.cleaned_data['senderMessage'],)

        msg = email.message_from_string(message)
        
        msg['From'] = form.cleaned_data['senderEmail']
        msg['To'] = emailTo
        msg['Subject'] = sourceFrom

        #send the email using multiprocessing
        t1 = Thread(target = self.sendEmailNow_Thread,
        args = (form.cleaned_data['senderEmail'], emailTo, msg,) )
        t1.start()

        if form.cleaned_data['ccSender']:
            #Create the email body to sender

            message = '''Dear %s,
            Thanks for reaching out to us. Below is your message that we have received. We will get back to you soon. 

            Thanks!

            Best regards,
            Hidden Dimsum

            Message
            %s''' %(form.cleaned_data['senderName'], form.cleaned_data['senderMessage'])
            
            msg = email.message_from_string(message)
            msg['From'] = emailTo 
            msg['To'] = form.cleaned_data['senderEmail']
            msg['Subject'] = 'Receipt of your message - Hidden Dimsum'

            #Send message. To minimize the wait time send email using multiprocessing
            t2 = Thread(target = self.sendEmailNow_Thread,
            args = (emailTo, form.cleaned_data['senderEmail'], msg,) )
            t2.start()
    
    def sendEmailNow_Thread(self, emailFrom, emailTo, msg):
        
        with open('static/emailCred.txt','r') as f:
            cred = json.load(f)

        smtpObj = smtplib.SMTP(host=cred['host'], port = cred['port'])
        smtpObj.starttls()
        smtpObj.login(cred['emailName'], cred['password'])
        smtpObj.sendmail(emailFrom, emailTo, msg.as_string())
        smtpObj.quit()