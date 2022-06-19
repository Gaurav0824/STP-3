from flask import Flask, render_template
from flask.templating import render_template_string
from flask import Flask, render_template, redirect, request, url_for
import json
import os

from flask.helpers import url_for
from jinja2.utils import urlize

app = Flask(__name__)

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@app.route('/graph.html')
def homeg():
    return render_template('graph.html')


@app.route('/graph.json')
def homegjson():
    return render_template('graph.json')


@app.route('/force.html')
def homef():
    return render_template('force.html')


@app.route('/force.js')
def homefjs():
    return render_template('force.js')


@app.route('/d3.v2.js')
def d3v2():
    return render_template('https://d3js.org/d3.v2.js')


# @app.route('/<name>')
# def home4(name):
#     return str(json.dumps(json.loads(nodes[0][3].decode()), indent=4))


def map_func(name):
    import sqlite3
    conn = sqlite3.connect('friends.sqlite')
    cur = conn.cursor()
    cur.execute(''' select data from People where name = ? ''', (name,))
    try:
        data = cur.fetchone()[0]
    except:
        pass
    # print(data[0])
    try:
        js = json.loads(data)
    except:
        pass
    cur.close()
    try:
        return str(js)
    except:
        return "Null"


if __name__ == '__main__':
    app.run(debug=False, port=5500)
