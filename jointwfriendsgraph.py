from os import abort
import sqlite3
import os


def jointwfriendsgraph():

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    APP_TEMPLATE = os.path.join(APP_ROOT, 'templates')

    conn = sqlite3.connect(APP_ROOT+'/friends.sqlite')
    cur = conn.cursor()

    print("Creating JSON output on friends.js...")
    # howmany = int(input("How many nodes? "))
    try:
        cur.execute('''SELECT COUNT(from_id) as inbound,to_id,name FROM People JOIN Follows ON People.id=Follows.to_id GROUP BY id ORDER BY id,inbound''')
    except:
        graph = open(APP_TEMPLATE+'/graph.json', 'w')  # ===================
        graph.write('')
        graph.close()
        return
        
    graph = open(APP_TEMPLATE+'/graph.json', 'w')  # ===================

    nodes = list()
    for row in cur:
        nodes.append(row)
        # if len(nodes) > howmany:
        #     break

    graph.write('{"nodes":[\n')
    count = 0
    map = dict()
    for row in nodes:
        # print(row, "\n")
        if count > 0:
            graph.write(',\n')
        graph.write('{' + '"name":"'+str(row[2]) + '"}')
        # +'",'+'"group":"'+str(row[1])+'"}')
        map[row[1]] = count
        count = count + 1
    graph.write('],\n')

    graph.write('"links":[\n')
    cur.execute('''SELECT DISTINCT from_id, to_id FROM Follows''')
    count = 0
    for row in cur:
        if row[0] not in map or row[1] not in map:
            continue
        if count > 0:
            graph.write(',\n')
        graph.write('{"source":'+str(map[row[0]]) +
                    ',"target":'+str(map[row[1]]) + '}')
        # +',"value":3}')
        # print(row, '\n')
        count = count + 1
    graph.write(']}')
    graph.flush()
    graph.close()
    cur.close()
    print("Open graph.html in a browser to view the visualization")

