import json
import sys
from scapy.all import *


def summary(packet):
    summary_str = str(packet)
    paramList = summary_str.split(' ')
    summaryMap = {}
    for i in paramList:
        if 'TCP' in i:
            tmp = i.split(':')
            summaryMap.get(tmp[0], )



if __name__ == "__main__":
    # sys.argv[0] is a name of python code
    input_timeout = sys.argv[1]
    packet = sniff(timeout = int(input_timeout))
