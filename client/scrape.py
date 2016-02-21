#!/usr/bin/python
from scapy.all import *
from uuid import getnode as get_mac
import requests
import time

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

ROUTERS = []
ROUTER_DATA = {}
HANDSHAKE_DONE = False

URL="http://159.203.87.28"
URL_HANDSHAKE=URL+"/data/handshake"
URL_ROUTER=URL+"/data/router"
URL_DEVICE=URL+"/data/device"

def PacketHandler(pkt):
    global ROUTERS
    global HANDSHAKE_DONE
    global ROUTER_DATA
    if pkt.haslayer(Dot11):
        print(ROUTERS)
        # if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE and ( pkt.addr2.lower() in WHITELIST or pkt.addr2.upper() in WHITELIST):
        # if pkt.addr2.lower() in WHITELIST or pkt.addr2.upper() in WHITELIST or pkt.addr1.lower() in WHITELIST or pkt.addr1.lower() in WHITELIST:
        if len(ROUTERS)!=0:
            if pkt.addr2 and pkt.subtype!=8 and (pkt.addr2.lower() in ROUTERS or pkt.addr2.upper() in ROUTERS):
                RouterPacket(pkt)
                if len(ROUTER_DATA)>=2:
                    print(ROUTER_DATA)
                    HANDSHAKE_DONE=True
                    ROUTERS=[]
        elif pkt.addr2 and pkt.subtype != 8:
            PrintPacket(pkt)

def SigStrength(pkt):
    try:
        extra = pkt.notdecoded
    except:
        extra = None 
    if extra!=None:
        signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
    return signal_strength

def RouterPacket(pkt):
    global ROUTER_DATA
    signal_strength = SigStrength(pkt)
    print(signal_strength)
    ROUTER_DATA[pkt.addr2]=signal_strength

def PrintPacket(pkt):
    signal_strength = SigStrength(pkt)
    mac=get_mac()
    mac=':'.join(("%12X" % mac)[i:i+2] for i in range(0,12,2))
    mac=mac.lower()
    timestamp=int(time.time())
    print ("%s %s %s %s %s" % (sys.argv[1],timestamp, mac, pkt.addr2, signal_strength))
    
    # POST TO SERVER
    payload={'mac':pkt.addr2,'router':mac,'signal_strength':signal_strength,'timestamp':timestamp}
    r = requests.post(URL_DEVICE,data=payload)
    print(r.status_code)
    # print "Target: %s Source: %s SSID: %s RSSi: %d"%(pkt.addr3,pkt.addr2,pkt.getlayer(Dot11ProbeReq).info,signal_strength)

def handshake():
    global ROUTERS
    global HANDSHAKE_DONE
    global ROUTER_DATA
    mac = get_mac()
    mac=':'.join(("%012X" % mac)[i:i+2] for i in range(0,12,2))
    mac=mac.lower()
    payload={'mac':mac}
    r = requests.post(URL_HANDSHAKE,data=payload)
    while(1):
        time.sleep(1)
        r = requests.get(URL_HANDSHAKE)
        data=r.json()
        print(data)
        if(len(data)==3):
            break
    data=requests.get(URL_HANDSHAKE).json()
    data.remove(mac)
    ROUTERS=data
    while not(HANDSHAKE_DONE):
        sniff(iface=sys.argv[1],prn=PacketHandler,count=10)
    payload=ROUTER_DATA
    payload["from"]=mac
    r = requests.post(URL_ROUTER,data=payload)

def main():
    from datetime import datetime
    print ("[%s] Starting scan"%datetime.now())
    handshake()
    sniff(iface=sys.argv[1],prn=PacketHandler)
    
if __name__=="__main__":
    main()
