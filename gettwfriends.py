import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import sqlite3
import ssl
import os   


def gettwfriends(acct, count):

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    count = int(count)

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    USER_URL = 'https://api.twitter.com/1.1/users/lookup.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    conn = sqlite3.connect(APP_ROOT+'\\friends.sqlite')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS People
                                (id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                                name           TEXT UNIQUE,
                                data             TEXT DEFAULT NULL,
                                retrieved    INTEGER  DEFAULT (0) CHECK (retrieved in (0,1) ) )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Follows
                                (from_id       INTEGER,
                                to_id              INTEGER,
                                UNIQUE        (from_id, to_id))''')

    conn.commit()

    while True:
        # acct = input('Enter a Twitter account, or quit: ')
        # if (acct == 'quit'):
        #     break
        count = count - 1
        if count < 0:
            break
        if (len(acct) < 1):
            cur.execute(
                'SELECT id, name FROM People WHERE retrieved=0 LIMIT 1')
            try:
                (id, acct) = cur.fetchone()
            except:
                print('No unretrieved Twitter accounts found')
                # continue
        else:
            cur.execute(
                'SELECT id FROM People WHERE name = ? LIMIT 1', (acct, ))
            try:
                id = cur.fetchone()[0]
            except:
                cur.execute('''INSERT OR IGNORE INTO People
                            (name, retrieved) VALUES (?, 0)''', (acct, ))
                conn.commit()
                if cur.rowcount != 1:
                    print('Error inserting account:', acct)
                    continue
                id = cur.lastrowid
                try:
                    url2 = twurl.augment(USER_URL, {'screen_name': acct})
                    try:
                        connection2 = urllib.request.urlopen(url2, context=ctx)
                    except Exception as err2:
                        print('Failed to Retrieve #USER', err2)
                        break
                    data2 = connection2.read().decode()
                    headers2 = dict(connection2.getheaders())
                    print('Remaining user_lookup',
                          headers2['x-rate-limit-remaining'])
                    try:
                        js2 = json.loads(data2)[0]
                        save = json.dumps(js2).encode()
                    except:
                        print('Unable to parse json')
                        print(data2)
                        break
                    cur.execute('UPDATE People SET data=? WHERE name=?',
                                (memoryview(save), acct, ))
                    conn.commit()
                except:
                    print('Error retrieving User data')
                    continue
        if count > 5:
            racct = count
        else:
            racct = 200
        url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': racct})
        print('Retrieving account', acct)

        try:
            connection = urllib.request.urlopen(url, context=ctx)
        except Exception as err:
            print('Failed to Retrieve', err)
            break

        data = connection.read().decode()
        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'])

        try:
            js = json.loads(data)
        except:
            print('Unable to parse json')
            print(data)
            break

        if 'users' not in js:
            print('Incorrect JSON received')
            print(json.dumps(js, indent=4))
            continue

        cur.execute('UPDATE People SET retrieved=1 WHERE name = ?', (acct, ))
        countnew = 0
        countold = 0
        for u in js['users']:
            friend = u['screen_name']
            print(friend)
            cur.execute('SELECT id FROM People WHERE name = ? LIMIT 1',
                        (friend, ))
            try:
                friend_id = cur.fetchone()[0]
                countold = countold + 1
            except:
                cur.execute('''INSERT OR IGNORE INTO People (name, data,retrieved)
                            VALUES (?,?, 0)''', (friend, memoryview(json.dumps(u).encode()), ))
                conn.commit()
                if cur.rowcount != 1:
                    print('Error inserting account:', friend)
                    continue
                friend_id = cur.lastrowid
                countnew = countnew + 1
            cur.execute('''INSERT OR IGNORE INTO Follows (from_id, to_id)
                        VALUES (?, ?)''', (id, friend_id))
        cur.execute('''INSERT OR IGNORE INTO Follows (from_id, to_id)
                    VALUES (?, ?)''', (id, id))
        print('New accounts=', countnew, ' revisited=', countold)
        print('Remaining', headers['x-rate-limit-remaining'])
        conn.commit()
        acct = ""
    cur.close()

def clear():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(APP_ROOT+'\\friends.sqlite')
    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS People''')
    cur.execute('''DROP TABLE IF EXISTS Follows''')
    conn.commit()
    cur.close()
