import sqlite3
import datetime

class registerEmail:
    def __init__(self):
        sqlstr = '''CREATE TABLE IF NOT EXISTS registerEmail (id integer PRIMARY KEY,
        emailAddress text NOT NULL,
        dateRegistered text NOT NULL,
        notifyTopic text NOT NULL)
        '''
        try:
            self.conn = sqlite3.connect('subscriptionEmail.db')
            c = self.conn.cursor()
            c.execute(sqlstr)
        except:
            self.conn.close()
            self.conn = False
    
    def insertEmailToDatabase(self, email, notifyTopic):
        '''
            Given email as a string and notifyTopic which is the area / web page that email was inserted to form, the two 
            information together with date will be inserted into the data base.
            Both email and notifyTopic are str
        '''
        dateStampStr = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        sqlStr = f'''INSERT INTO registerEmail (emailAddress, dateRegistered, notifyTopic)
        VALUES('{email}','{dateStampStr}','{notifyTopic}')
        '''
        c = self.conn.cursor()
        c.execute(sqlStr)
        self.conn.commit()
        self.conn.close()
        
        

        

