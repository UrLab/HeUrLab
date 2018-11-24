import requests
import redis
import json
import os
import logging
from xml.etree import ElementTree
from time import sleep
from datetime import datetime

from config import INTERESTING_HALTS, URL, LOG_LEVEL

logger = logging.getLogger(__name__)

db = redis.StrictRedis(host='localhost', port=6379, db=1)


def timing():
    for halt in INTERESTING_HALTS:
        res = []
        for halt_id in INTERESTING_HALTS[halt][0]:
            data = asking(halt, halt_id)
            try:
                if data[0][0].strip() == "72":
                    data = [data[0]]
            except IndexError:
                data = [['72', 'NO BK FOR YOU', '-1']]
            res.extend(data)
        res = sorted(res, key=lambda x: x[0])
        res = json.dumps(res)
        db.set(halt, res)
    last_update = datetime.now().isoformat()
    db.set("last_updated", last_update)


def asking(halt, halt_id):
    # With no timeout, if internet is disabled while the requests are going out,
    #   they will hang indefinetely
    response = requests.get(URL.format(halt_id), timeout=10)
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
    logging.basicConfig(
        filename="{}/stib_backend.log".format(os.path.dirname(os.path.abspath(__file__))),
        level=LOG_LEVEL,
        filemode='a',
        format="%(levelname)s:%(name)s:[%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.info(" ")
    logging.info("-" * 50)
    logging.info(" ")
    while True:
        try:
            logger.info("Trying to scrape stib")
            timing()
            logger.info("Scraped stib")
            db.set("backend_state", "")
            sleep(10)
        except (
            requests.ReadTimeout, requests.ConnectTimeout,
            requests.ConnectionError
        ) as e:
            logger.error(type(e).__name__)
            db.set("backend_state", type(e).__name__)
            sleep(30)
        except Exception as e:
            db.set("backend_state", "I deaded :(")
            logger.exception("New phone, who dis?")
            raise
