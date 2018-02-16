import requests
from xml.etree import ElementTree
from config import INTERESTING_HALTS, URL
import redis
import json
from time import sleep

db = redis.StrictRedis(host='localhost', port=6379, db=1)

def timing():
    for halt in INTERESTING_HALTS:
        res = []
        for halt_id in INTERESTING_HALTS[halt][0]:
            res.extend(asking(halt, halt_id))
        res = sorted(res, key = lambda x: x[0])
        res = json.dumps(res)
        db.set(halt, res)

def asking(halt, halt_id):
    response = requests.get(URL.format(halt_id))
    if response.status_code == 200:
        res = []
        tree = ElementTree.fromstring(response.content)
        all_stop = list(tree.getiterator(tag='waitingtime'))
        for each in all_stop:
            info = {i.tag : i.text for i in each}
            if info["line"] in INTERESTING_HALTS[halt][1] and info["destination"] != "ULB":
                res.append([info["line"], info["destination"], info["minutes"]])
        return res
    else :
        return -1

if __name__=="__main__":
    while True:
        timing()
        print("got data !")
        sleep(10)
