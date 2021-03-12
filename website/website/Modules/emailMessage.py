import smtplib
import email
import json
import multiprocessing

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
        p1 = multiprocessing.Process(target = self.sendEmailNow_Multiprocessing,
        args = (form.cleaned_data['senderEmail'], emailTo, msg,) )
        p1.start()

        #sucessSentToTarget = self.sendEmailNow(emailFrom = form.cleaned_data['senderEmail'],
        #emailTo = emailTo, msg = msg)

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
            p2 = multiprocessing.Process(target = self.sendEmailNow_Multiprocessing,
            args = (emailTo, form.cleaned_data['senderEmail'], msg,) )
            p2.start()
            #successCCsent = self.sendEmailNow(emailFrom = emailTo,
            #emailTo = form.cleaned_data['senderEmail'], msg = msg)
        #else:
          #  successCCsent = None

        #self.status = (sucessSentToTarget, successCCsent)

    def sendEmailNow(self, emailFrom, emailTo, msg):
        with open('static/emailCred.txt','r') as f:
            cred = json.load(f)
        try:
            smtpObj = smtplib.SMTP(host=cred['host'], port = cred['port'])
            smtpObj.starttls()
            smtpObj.login(cred['emailName'], cred['password'])
            smtpObj.sendmail(emailFrom, emailTo, msg.as_string())
            smtpObj.quit()
            status = True
        except:
            status = False
        
        return status
    
    def sendEmailNow_Multiprocessing(self, emailFrom, emailTo, msg):
        with open('static/emailCred.txt','r') as f:
            cred = json.load(f)

        smtpObj = smtplib.SMTP(host=cred['host'], port = cred['port'])
        smtpObj.starttls()
        smtpObj.login(cred['emailName'], cred['password'])
        smtpObj.sendmail(emailFrom, emailTo, msg.as_string())
        smtpObj.quit()
        


