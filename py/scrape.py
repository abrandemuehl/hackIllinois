#!/usr/bin/python
from scapy.all import *
from uuid import getnode as get_mac
import requests
import time

PROBE_REQUEST_TYPE=0
PROBE_REQUEST_SUBTYPE=4

WHITELIST = ['6c:72:e7:51:3a:f1'] # Replace this with your phone's MAC address


def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        # if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype == PROBE_REQUEST_SUBTYPE and ( pkt.addr2.lower() in WHITELIST or pkt.addr2.upper() in WHITELIST):
        # if pkt.addr2.lower() in WHITELIST or pkt.addr2.upper() in WHITELIST or pkt.addr1.lower() in WHITELIST or pkt.addr1.lower() in WHITELIST:
        if pkt.addr2 and pkt.subtype != 8:
            PrintPacket(pkt)

def PrintPacket(pkt):
    try:
        extra = pkt.notdecoded
    except:
        extra = None
    if extra!=None:
        signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
        print ("No signal strength found")
    mac=get_mac()
    timestamp=int(time.time())
    print ("%s %s %s %s %s" % (sys.argv[1],timestamp, mac, pkt.addr2, signal_strength))
    
    # POST TO SERVER
    payload={'mac':pkt.addr2,'router':mac,'signal_strength':signal_strength,'timestamp':timestamp}
    r = requests.post("http://159.203.87.28/data",data=payload)
    print(r.status_code)
    # print "Target: %s Source: %s SSID: %s RSSi: %d"%(pkt.addr3,pkt.addr2,pkt.getlayer(Dot11ProbeReq).info,signal_strength)

def main():
    from datetime import datetime
    print ("[%s] Starting scan"%datetime.now())
    print ("Scanning for:")
    print ("\n".join(mac for mac in WHITELIST))
    
    sniff(iface=sys.argv[1],prn=PacketHandler)
    
if __name__=="__main__":
    main()
