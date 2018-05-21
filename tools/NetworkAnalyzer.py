from scapy.all import *
import json
import sys

def summary(p):
    summaryStr = str(p)
    summaryStr = summaryStr.replace('<', '').replace('>', '').replace('Sniffed: ', '')
    paramList = summaryStr.split(' ')
    summaryMap = {}

    for i in paramList:
        tmp = i.split(':')
        summaryMap[tmp[0]] = tmp[1]

    return summaryMap



def extractSummary(summary_str):
    pass

def cleanPayload(p):
    p = str(p)
    return p.split('Raw')[0].split("Padding")[0].replace('|','\n').strip('<')\
            .strip('bound method Ether.show of ').replace('>','').replace('[<','[')\
            .replace('\n<','<').replace('<','\n')



if __name__ == "__main__":
    # sys.argv[0] is python file name.
    input_timeout = sys.argv[1] # sniffing time

    packet = sniff(timeout=int(input_timeout))

    l2CountingMap = {}
    l3CountingMap = {}
    srcIpCountingMap = {}
    dstIpCountingMap = {}
    srcPortCountingMap = {}
    dstPortCountingMap = {}

    for i in range(len(packet)):
        try:
            l2 = packet[i][0]
            l3 = packet[i][1]
            srcIp = packet[i][IP].src
            dstIp = packet[i][IP].dst
            srcPort = packet[i][IP].sport
            dstPort = packet[i][IP].dport

            l2Count = l2CountingMap.get(l2, 0)
            l3Count = l3CountingMap.get(l3, 0)
            srcIpCount = srcIpCountingMap.get(srcIp, 0)
            dstIpCount = dstIpCountingMap.get(dstIp, 0)
            srcPortCount = srcPortCountingMap.get(srcPort, 0)
            dstPortCount = dstPortCountingMap.get(dstPort, 0)

            l2CountingMap[l2] = l2Count + 1
            l3CountingMap[l3] = l3Count + 1
            srcIpCountingMap[srcIp] = srcIpCount + 1
            dstIpCountingMap[dstIp] = dstIpCount + 1
            srcPortCountingMap[srcPort] = srcPortCount + 1
            dstPortCountingMap[dstPort] = dstPortCount + 1





#    summary = packet.summary()

    #print(summary)
    #print(cleanPayload(packet))
    #testMap = summary(packet)
    #print(testMap)
    a = summary(packet)
    print(a)
    print(str(a))



