from flask import Flask, render_template
from config import INTERESTING_HALTS, URL
import redis
import json

app = Flask(__name__)
db = redis.StrictRedis(host='localhost', port=6379, db=1)

@app.route("/")
def index():
    time_info = {}
    for halt in INTERESTING_HALTS:
        stored = json.loads(db.get(halt))
        if -1 in stored:
            return render_template("error.html")
        time_info[halt] = stored
    return render_template("index.html", info = time_info, walk = INTERESTING_HALTS, full = [])

@app.route("/style.css")
def style():
    with open("css/style.css", "r") as f:
        return f.read(), 200, {'Content-Type': 'text/css; charset=utf-8'}
