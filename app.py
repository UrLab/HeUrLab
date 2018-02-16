from flask import Flask, render_template
import requests
from xml.etree import ElementTree
from config import INTERESTING_HALTS, URL

app = Flask(__name__)

def sorting(dic):
    if dic != -1:
        for i in dic:
            dic[i] = sorted(dic[i], key = lambda x: x[0])
    return dic

def timing(interesting_halts):
    res = {}
    for halt in interesting_halts :
        res[halt] = []
        for halt_id in interesting_halts[halt][0]:
            response = requests.get(URL.format(halt_id))
            if response.status_code == 200:
                tree = ElementTree.fromstring(response.content)
                all_stop = list(tree.getiterator(tag='waitingtime'))
                for each in all_stop:
                    info = {i.tag : i.text for i in each}
                    if info["line"] in interesting_halts[halt][1] and info["destination"] != "ULB":
                        res[halt].append([info["line"], info["destination"], info["minutes"]])
            else :
                res = -1
    res = sorting(res)
    return res

@app.route("/")
def index():
    time_info = timing(INTERESTING_HALTS)
    if time_info != -1 :
        return render_template("index.html", info = timing(INTERESTING_HALTS), walk = INTERESTING_HALTS, full = [])
    else :
        return render_template("error.html")

@app.route("/style.css")
def style():
    with open("css/style.css", "r") as f:
        return f.read(), 200, {'Content-Type': 'text/css; charset=utf-8'}
