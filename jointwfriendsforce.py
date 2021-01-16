import sqlite3

conn = sqlite3.connect('friends.sqlite')
cur = conn.cursor()

print("Creating JSON output on friends.js...")
howmany = int(input("How many nodes? "))

cur.execute('''SELECT COUNT(from_id) as inbound,to_id,name FROM People JOIN Follows ON People.id=Follows.to_id GROUP BY id ORDER BY id,inbound''')

force = open('spider.js', 'w')  # ===================
nodes = list()
for row in cur:
    nodes.append(row)
    if len(nodes) > howmany:
        break

force.write('spiderJson = {"nodes":[\n')
count = 0
map = dict()
for row in nodes:
    print(row,"\n")
    if count > 0:
        force.write(',\n')
    rank = row[0]*2
    force.write('{'+'"weight":'+str(row[0])+','+'"rank":'+str(rank)+',' +' "id":'+str(row[1])+', "name":"'+row[2]+'"}')
    map[row[1]] = count
    count = count + 1
force.write('],\n')

force.write('"links":[\n')
cur.execute('''SELECT DISTINCT from_id, to_id FROM Follows''')
count = 0
for row in cur:
    if row[0] not in map or row[1] not in map:
        continue
    if count > 0:
        force.write(',\n')
    force.write('{"source":'+str(map[row[0]])+',"target":'+str(map[row[1]]) +',"value":3}')
    print(row,'\n')
    count = count + 1
force.write(']}')

force.close()
cur.close()
print("Open force.html in a browser to view the visualization")
# =======================================================================================