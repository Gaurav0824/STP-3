from flask import *
from login_signup import *
from gettwfriends import *
from jointwfriendsgraph import *
import json
import os
import sqlite3

loginsignup = login_signup()

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/login3")
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        email = request.form.get('username')
        pwd = request.form.get('password')
        # print(email, pwd)
        if email and pwd and loginsignup.login_user(login_details={"email": email, "pwd": pwd}):
            return redirect('/home')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login3.html", error=error)


@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        pwd = request.form.get('password')
        # print(email, fname, lname, pwd)
        if email and pwd and fname and loginsignup.signup_user(signup_details={"email": email, "pwd": pwd, "fname": fname, "lname": lname}):
            return redirect('/')
        else:
            error = "Signup unsuccessful, User Already Exists"
    return render_template("signup.html", error=error)


@app.route('/home', methods=['GET', 'POST'])
def home():
    error = ""
    name = loginsignup.fname  # +" "+loginsignup.lname
    return render_template("home.html", name=name, error=error)


@app.route('/graph2', methods=['GET', 'POST'])
def graph():
    # if request.method == 'POST':
    if "twfriends_submit" in request.form:
        acct = request.form.get('twacct')
        count = request.form.get('count')
        # print(request.form)
        if len(count) < 1:
            count = 1
        gettwfriends(acct, count)
        jointwfriendsgraph()
    if "clear" in request.form:
        clear()
        jointwfriendsgraph()
    return render_template("graph2.html")


@app.route('/graph2/<name>')
def profile(name):
    profile_tweets = "https://twitter.com/"+name+"?ref_src=twsrc%5Etfw"
    likes_tweets = "https://twitter.com/"+name+"/likes?ref_src=twsrc%5Etfw"
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(APP_ROOT+'\\friends.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT data FROM People where name = ? ", (name,))
    try:
        data = cur.fetchone()[0]
    except:
        print("NADA")
        exit()
    js = json.loads(data)
    profilepic = js['profile_image_url']

    return render_template("profile.html", data=js, profile_tweets=profile_tweets, likes_tweets=likes_tweets, profilepic=profilepic)


@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    name = ''
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(APP_ROOT+'\\friends.sqlite')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('twacct', '')
        if 'add' in request.form:
            try:
                cur.execute(
                    '''CREATE TABLE IF NOT EXISTS monitor ( name TEXT )''')
                cur.execute('INSERT INTO monitor VALUES (?)', (name,))
                conn.commit()
            except:
                pass

        elif 'delete' in request.form:
            try:
                cur.execute('DELETE FROM monitor WHERE name = ?', (name,))
                conn.commit()
            except:
                pass

    # profile_tweets = "https://twitter.com/"+name+"?ref_src=twsrc%5Etfw"
    # likes_tweets = "https://twitter.com/"+name+"/likes?ref_src=twsrc%5Etfw"

    cur.execute('SELECT * FROM monitor')
    data = cur.fetchall()
    profile = []
    likes = []
    for row in data:
        profile.append("https://twitter.com/"+row[0]+"?ref_src=twsrc%5Etfw")
        likes.append("https://twitter.com/" +
                     row[0]+"/likes?ref_src=twsrc%5Etfw")

    print(data, len(data), profile, likes)
    return render_template('monitor.html', data=data, data_len=len(data), profile=profile, likes=likes)


@app.route('/htmllab', methods=['GET', 'POST'])
def htmllab():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    if request.method == 'POST':
        data = str(request.form.get('code'))
        print(data)
        with open(APP_ROOT+'\Templates\\temp.html', 'w') as file:
            file.write(data)
        return render_template('htmllab.html', data=data)
    with open(APP_ROOT+'\Templates\\temp.html', 'w') as file:
        file.write('')
    return render_template('htmllab.html')


@app.route('/graph.json')
def homegjson():
    return render_template('graph.json')


@app.route('/codemirror.js')
def codemirrorjs():
    return render_template('codemirror.js')


@app.route('/temp.html')
def temphtml():
    return render_template('temp.html')


@app.route('/htmlmixed.js')
def htmlmixed():
    return render_template('htmlmixed.js')


app.run(debug=True)
