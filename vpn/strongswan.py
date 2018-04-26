import os
import sys
import subprocess
import copy


# path of ipsec.conf
IPSEC_CONFIG_PATH = "/etc/ipsec.conf"
IPSEC_SECRETS_PATH = "/etc/ipsec.secrets"
TUNNEL_CONFIG_KEY = ["conn", "left", "leftsubnet", "right", "rightsubnet", "ikelifetime", "lifetime", "keyexchange", "dpddelay", "dpdtimeout", "ike", "esp", "keyingtries""dpdaction", "authby", "auto", "type"]
TUNNEL_CONFIG_PARAMETER_COUNT = 8
TUNNEL_CONFIG_FORMAT = "###TUNNEL_START###\nconn %s\n\tleft=%s\n\tleftsubnet=%s\n\tright=%s\n\trightsubnet=%s\n\tikelifetime=%s\n\tlifetime=%s\n\tkeyexchange=%s\n\t"
DEFAULT_CONFIG = "dpddelay=30\n\tdpdtimeout=120\n\tike=aes256-sha2_256-modp1024!\n\tesp=aes256-sha2_256!\n\tkeyingtries=0\n\tdpdaction=restart\n\tauthby=secret\n\tauto=start\n\ttype=tunnel\n###TUNNEL_END###\n\n"

def parseConfig(configStr):
    configList = configStr.split(",")
    return configList

def setTunnel(tunnelConfigList):
    tunnelConfigStr = copy.deepcopy(TUNNEL_CONFIG_FORMAT)
    tunnelConfigStr = tunnelConfigStr % tuple(tunnelConfigList)
    tunnelId = tunnelConfigList[0]

    #print(tunnelConfigStr+DEFAULT_CONFIG)
    tunnelConfigStr = tunnelConfigStr + DEFAULT_CONFIG
    
    f = open(IPSEC_CONFIG_PATH, "a")
    f.write(tunnelConfigStr)
    f.close()

    f = open(IPSEC_SECRETS_PATH, "a")


    result = subprocess.check_output("ipsec update", shell=True)
    print(result)
    #result = subprocess.check_output("ipsec up %s"%(tunnelId), shell=True)
    #print(result)


if __name__ == "__main__":
    print("Number of arguments : ", len(sys.argv))
    print("Argument List : ", str(sys.argv))
    print(sys.argv[1])
    tempConfig = parseConfig(sys.argv[1])
    setTunnel(tempConfig)

'''    
    command = sys.argv[1]

    if command == "create":
        setTunnel(sys.argv[2])
    elif command == "update":
        pass
    elif command == "delete":
        pass
    else:
        print("ERROR")
''' 
