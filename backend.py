import requests
from xml.etree import ElementTree
from config import INTERESTING_HALTS, URL
import redis
import json
from time import sleep
import sys
import traceback

db = redis.StrictRedis(host='localhost', port=6379, db=1)


def timing():
    for halt in INTERESTING_HALTS:
        res = []
        for halt_id in INTERESTING_HALTS[halt][0]:
            data = asking(halt, halt_id)
            if data[0][0].strip() == "72":
                data = [data[0]]
            res.extend(data)
        res = sorted(res, key=lambda x: x[0])
        res = json.dumps(res)
        db.set(halt, res)


def asking(halt, halt_id):
    response = requests.get(URL.format(halt_id))
    if response.status_code == 200:
        res = []
        tree = ElementTree.fromstring(response.content)
        all_stop = list(tree.getiterator(tag='waitingtime'))
        for each in all_stop:
            info = {i.tag: i.text for i in each}
            if info["line"] in INTERESTING_HALTS[halt][1] and info["destination"] != "ULB":
                if len(info["minutes"]) == 1:
                    info["minutes"] = " " + info["minutes"]
                res.append([info["line"], info["destination"], info["minutes"]])
        return res
    else:
        return -1


if __name__ == "__main__":
    while True:
        try:
            timing()
            print("got data !")
            sleep(10)
        except: # NOQA
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # exc_type below is ignored on 3.5 and later
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
            sleep(20)
