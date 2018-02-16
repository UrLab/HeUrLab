URL = "http://m.stib.be/api/getwaitingtimes.php?halt={}"

INTERESTING_HALTS = {
    "CIM. D'IXELLES" : [["3514","3558"], ["95"], "10"],
    "ULB1" : [["5407"], ["94", "25", "71"], "3"],
    "ULB2" : [["3556","3513","5462"], ["94","25","71","72"], "3"],
    "BUYL" : [["3481", "3480"], ["7"], "12"],
    "DELTA" : [["8232","8231"], ["5"], "25"]
}

# Halt_name : [[Halt_id's], [Interesting_lines], walking_time]
