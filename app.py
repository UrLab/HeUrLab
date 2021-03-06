from flask import Flask, render_template
from config import INTERESTING_HALTS
import redis
import json

app = Flask(__name__)
db = redis.StrictRedis(host='localhost', port=6379, db=1, charset="utf-8", decode_responses=True)


@app.route("/")
def index():
    time_info = {}
    for halt in INTERESTING_HALTS:
        stored = json.loads(db.get(halt))
        if -1 in stored:
            return render_template("error.html")
        time_info[halt] = stored

    last_updated = db.get("last_updated")
    backend_state = db.get("backend_state")
    if backend_state is None:
        backend_state = ""

    return render_template("index.html", info=time_info, walk=INTERESTING_HALTS, full=[], last_updated=last_updated, backend_state=backend_state)


@app.route("/style.css")
def style():
    with open("css/style.css", "r") as f:
        return f.read(), 200, {'Content-Type': 'text/css; charset=utf-8'}
