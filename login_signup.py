import sqlite3
import os


class login_signup:

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):

        conn = sqlite3.connect(login_signup.APP_ROOT+'\\accounts.sqlite')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS UserData( 
                                    sno INTEGER PRIMARY KEY AUTOINCREMENT,
                                    email TEXT UNIQUE,
                                    fname TEXT,
                                    lname TEXT,
                                    pwd TEXT,
                                    UNIQUE  (email,pwd) )''')
        conn.commit()
        cur.close()

    def login_user(self, login_details):
        """
        login_details : dictionary
        """
        conn = sqlite3.connect(login_signup.APP_ROOT+'\\accounts.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT sno,fname,lname FROM UserData WHERE email=? AND pwd = ?',
                    (login_details['email'], login_details['pwd'], ))
        # print(login_details['email'], login_details['pwd'])
        self.email = login_details['email']
        self.pwd = login_details['pwd']
        try:
            id = cur.fetchone()
            try:
                self.sno = id[0]
                self.fname = id[1]
                self.lname = id[2]
            except:
                print ("No such user Exists")
                return False
            print(id)
            print("Login Successful")
            return True
        except:
            print("Incorrect Login Details")
            return False
        finally:
            cur.close()

    def signup_user(self, signup_details):

        conn = sqlite3.connect(login_signup.APP_ROOT+'\\accounts.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT sno FROM UserData WHERE email=? ',
                    (signup_details['email'],))

        try:
            id = cur.fetchone()[0]
            print("User Already Exists")
            print("Signup UN- Successful")
            return False

        except:
            cur.execute('INSERT INTO UserData(email,fname,lname,pwd) VALUES (?,?,?,?) ', (
                signup_details['email'], signup_details['fname'], signup_details['lname'], signup_details['pwd'], ))
            print("Signup Successful")
            conn.commit()
            return True

        finally:
            cur.close()
