import os
import sys
import subprocess
import copy
from collections import OrderedDict


# path of ipsec.conf
IPSEC_CONFIG_PATH = "/etc/ipsec.conf"
IPSEC_SECRETS_PATH = "/etc/ipsec.secrets"
IPSEC_CONFIG_FILE = '### ipsec.conf ###\nconfig setup\n\tcharondebug="all"\n\tuniqueids=yes\n\tstrictcrlpolicy=no\n\n'
IPSEC_SECRETS_FILE = '### ipsec.secrets ###\n\n'
TUNNEL_CONFIG_KEY = ["conn", "left", "leftsubnet", "right", "rightsubnet", "ikelifetime", "lifetime", "keyexchange", "dpddelay", "dpdtimeout", "ike", "esp", "keyingtries""dpdaction", "authby", "auto", "type"]
TUNNEL_CONFIG_LINE = len(TUNNEL_CONFIG_KEY)
TUNNEL_CONFIG_PARAMETER_COUNT = 8
TUNNEL_CONFIG_FORMAT = "conn %s\n\tleft=%s\n\tleftsubnet=%s\n\tright=%s\n\trightsubnet=%s\n\tikelifetime=%s\n\tlifetime=%s\n\tkeyexchange=%s\n\t"
DEFAULT_CONFIG = "dpddelay=30\n\tdpdtimeout=120\n\tike=aes256-sha2_256-modp1024!\n\tesp=aes256-sha2_256!\n\tkeyingtries=0\n\tdpdaction=restart\n\tauthby=secret\n\tauto=start\n\ttype=tunnel\n\n"


def initConfigFile():
    # init ipsec.conf file
    f = open(IPSEC_CONFIG_PATH, "w")
    f.write(IPSEC_CONFIG_FILE)
    f.close()

    #init ipsec.secrets
    f = open(IPSEC_SECRETS_PATH, "w")
    f.write(IPSEC_SECRETS_FILE)
    f.close()

def parseConfig(configStr):
    configList = configStr.split("#")
    return configList

def createTunnel(tunnelConfigList, psk):
    # TODO check paramater number

    tunnelConfigDict = OrderedDict(zip(TUNNEL_CONFIG_KEY, tunnelConfigList))
    tunnelConfigStr = copy.deepcopy(TUNNEL_CONFIG_FORMAT)
    tunnelConfigStr = tunnelConfigStr % tuple(tunnelConfigList)
    tunnelConfigStr = tunnelConfigStr + DEFAULT_CONFIG

    # TODO duplicate check
    f = open(IPSEC_CONFIG_PATH, "a")
    f.write(tunnelConfigStr)
    f.close()

    # add ###TUNNEL_ID###
    # add PSK 192.168.1.101 192.168.1.102 : PSK 'test123'
    secret = tunnelConfigDict["left"] + " " + tunnelConfigDict["right"] + " : PSK " + "'%s'"%(psk) + "\n\n"
    f = open(IPSEC_SECRETS_PATH, "a")
    f.write("###%s###\n"%(tunnelConfigDict["conn"]))
    f.write(secret)
    f.close()

    #runIpsecUpdate()

    #tunnelId = tunnelConfigList[0]
    #result = subprocess.check_output("ipsec up %s"%(tunnelId), shell=True)
    #print(result)

def deleteTunnel(tunnelId):
    # delete tunnel
    f = open(IPSEC_CONFIG_PATH, "r")
    tunnel_lines = f.readlines()
    f.close()

    for i in range(len(tunnel_lines)):
        if ("conn " + tunnelId) in tunnel_lines[i]:
            del tunnel_lines[i:i+TUNNEL_CONFIG_LINE+2]
            break

    f = open(IPSEC_CONFIG_PATH, "w")
    f.writelines(tunnel_lines)
    f.close()


    # delete secrets
    f = open(IPSEC_SECRETS_PATH, "r")
    secret_lines = f.readlines()
    f.close()

    for i in range(len(secret_lines)):
        if "###%s###"%(tunnelId) in secret_lines[i]:
            del secret_lines[i:i+3]
            break
    f = open(IPSEC_SECRETS_PATH, "w")
    f.writelines(secret_lines)
    f.close()


    runIpsecDown(tunnelId)


def runIpsecUpdate():
    result = subprocess.check_output("ipsec update", shell=True)
    print(result)

def runIpsecUp(tunnelId):
    result = subprocess.check_output("ipsec up %s"%(tunnelId), shell=True)
    print(result)

def runIpsecDown(tunnelId):
    result = subprocess.check_output("ipsec update", shell=True)
    print(result)
    result = subprocess.check_output("ipsec down %s"%(tunnelId), shell=True)



if __name__ == "__main__":
    print("Number of arguments : ", len(sys.argv))
    print("Argument List : ", str(sys.argv))
    for i in range(len(sys.argv)):
        print(sys.argv[i])

    command = sys.argv[1]

    if command == "create":
        config = parseConfig(sys.argv[2])
        createTunnel(config, sys.argv[3])
        runIpsecUpdate()
        print("[LOG] call create")
    elif command == "update":
        config = parseConfig(sys.argv[2])
        tunnelId = config[0]
    elif command == "delete":
        deleteTunnel(sys.argv[2])
        print("[LOG] call delete")
    elif command == "init":
        initConfigFile()
        print("[LOG] call init")
    elif command == "up":
        runIpsecUp(sys.argv[2])
        print("[LOG] up the tunnel")
    elif command == "down":
        runIpsecDown(sys.argv[2])
        print("[LOG] down the tunnel")
    elif command == "add":
        config = parseConfig(sys.argv[2])
        createTunnel(config, sys.argv[3]) 
    else:
        print("ERROR : StrongSwan python script")
