import requests
from xml.etree import ElementTree

URL = "http://m.stib.be/api/getwaitingtimes.php?halt="

interesting_halts = {
    "CIM. D'IXELLES" : [["3514","3558"], ["95"]],
    "ULB" : [["5407","3556","3513","5462"], ["94","25","71","72"]],
    "BUYL" : [["3481", "3480"], ["7"]],
    "DELTA" : [["8232","8231"], ["5"]]
}

for halt in interesting_halts :
    print(halt)
    for halt_id in interesting_halts[halt][0]:
        response = requests.get(URL + halt_id)
        if response.status_code == 200:
            tree = ElementTree.fromstring(response.content)
            all_stop = list(tree.getiterator(tag='waitingtime'))
            for each in all_stop:
                info = {i.tag : i.text for i in each}
                if info["line"] in interesting_halts[halt][1]:
                    print( "The next {} going to {} is in {} minutes.".format(info["line"], info["destination"], info["minutes"]))
