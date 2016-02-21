import math


#queue for timestamps, also a dictionary with MAC addresses
#time_dict = {}
#holds device MAC addresses, dictionary of timestamps, and signal strengths 
dict_storage = {}
#holds MAC addresses, timestamps, and final (x,y) coordinates; dict_coord[mac][n] where n = 0(timestamp), 1(x coord), 2(y coord)
dict_coordinates = {}
#holds router MAC Addresses, should hold 3 values max
router_addresses = {}
#router coordinates:

router1 = None
router2 = None
router3 = None

class Router(object):
    def __init__(self, x, y, mac):
        self.x = x
        self.y = y
        self.mac = mac
    def __str__(self):
        return str({"x": self.x, "y": self.y, "mac": self.mac})

def position_routers(router_distances):
    # Group the relationship by source mac
    # list of 
    # {'mac': ..., 'to': ..., 'signal': ...}
    routers = {}

    # Routers is of form
    # {'mac': {to1: signal,
    #          to2: signal,
    #          'mac': mac}}
    for distance in router_distances:
        if not routers.has_key(distance['mac']):
            routers[distance['mac']] = {}
        routers[distance['mac']]['mac'] = distance['mac']
        routers[distance['mac']][distance['to']] = distance['signal']

    mac_addresses = routers.keys()

    first = routers[mac_addresses[0]]
    print first
    second = routers[mac_addresses[1]]
    print second
    third = routers[mac_addresses[2]]
    print third

    global router1 
    router1 = Router(0, 0, first['mac'])
    print str(router1)

    # average the signals between the two
    firstToSecond = abs(first[second['mac']] + second[first['mac']]) / 2
    firstToThird = abs(first[third['mac']] + third[first['mac']]) / 2
    secondToThird = abs(second[third['mac']] + third[second['mac']]) / 2

    print firstToSecond
    print firstToThird
    print secondToThird
    # Set router2 on y axis
    global router2 
    router2 = Router(0, signalToDistance(firstToSecond), second['mac'])


    # Adjacent^2 + adjacent^2 - opposite^2
    theta = math.acos(float(firstToSecond**2 + firstToThird**2 - secondToThird**2) / 
            float(2 * firstToSecond * firstToThird))

    global router3 
    router3 = Router(firstToThird*math.cos(theta), firstToThird*math.sin(theta), third['mac'])

    router_addresses[router1.mac] = 0
    router_addresses[router2.mac] = 1
    router_addresses[router3.mac] = 2






#def routerAddress(router_mac_addr) :
#	if (len(router_addresses.keys()) < 3) :
#		if (not router_addresses.has_key(router_mac_addr)) :
#			router_addresses[router_mac_addr] = len(router_addresses.keys())
	

def checkForUpdates(mac_addr, timestamp, signal, router_addr):
	if (not dict_storage.has_key(mac_addr)):
		dict_storage[mac_addr] = {timestamp: [0, 0, 0]}	
		#time_dict[mac_addr] = [timestamp]
	if (not dict_storage[mac_addr].has_key(timestamp)) :
		dict_storage[mac_addr][timestamp] = [0, 0, 0]
		#time_dict[mac_addr].append(timestamp)
	dict_storage[mac_addr][timestamp][router_addresses[router_addr]] = signal
	
	if dict_storage[mac_addr][timestamp][0] != 0 and dict_storage[mac_addr][timestamp][1] != 0 and dict_storage[mac_addr][timestamp][2] != 0:
		output = dict_storage[mac_addr][timestamp]
		temp = sorted(dict_storage[mac_addr].keys(), key = lambda x: int(x))
		for i in range(len(temp)):
			if(int(temp[i]) < int(timestamp)):
				del dict_storage[temp[i]]
			else:
				break
		del dict_storage[mac_addr][timestamp]
		return (trilateration_x(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][1]),
			trilateration_y(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][2], dict_coordinates[mac_addr][1]),
			mac_addr)
	else:
		return None
	#if int(timestamp) > int(dict_coordinates[mac_addr][0]) :
	#	dict_coordinates[mac_addr][0] = timestamp
	#	dict_coordinates[mac_addr][1] = trilateration_x(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][1])
	#	dict_coordinates[mac_addr][2] = trilateration_y(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][2], dict_coordinates[mac_addr][1])
	#	temp = sorted(dict_storage[mac_addr].keys(), key = lambda x: int(x))
		#time_dict[mac_addr].sort(key = float) 
	#	while (1) :
	#		if (dict_storage[mac_addr][0] < timestamp) :
	#			#a = str (time_dict[mac_addr][0])
	#			#del time_dict[mac_addr][0]
	#			del dict_storage[mac_addr][0]
	#		else :
	#			break	
	#	del dict_storage[mac_addr][timestamp]
	#	return (dict_coordinates[mac_addr][1], dict_coordinates[mac_addr][2], mac_addr) #returns (x, y, MAC addr) as tuple
	#else: 
	#	print "delete node"
	#	print dict_storage[mac_addr][timestamp]
	#	del dict_storage[mac_addr][timestamp]
	#	return None


def trilateration_x(s1, s2) :

	x = (math.pow(s1, 2) - math.pow(s2, 2) + math.pow(router2.x, 2)) / (2 * router2.x)
	return x

def trilateration_y(s1, s3, trilat_x) :

	y = ((math.pow(s1, 2) - math.pow(s3, 2) + math.pow(router3.x, 2) + math.pow(router3.y, 2)) / (2 * router3.y)) - ((router3.x * trilat_x) / y3)
	return y

if __name__ == "__main__":
    router_distances = [
            {"mac": "1", "to": "2", "signal": -15},
            {"mac": "1", "to": "3", "signal": -15},
            {"mac": "2", "to": "1", "signal": -15},
            {"mac": "2", "to": "3", "signal": -15},
            {"mac": "3", "to": "1", "signal": -15},
            {"mac": "3", "to": "2", "signal": -15},
            ]
    position_routers(router_distances)
    print "Routers:"
    print str(router1)
    print str(router2)
    print str(router3)
    #routerAddress("1")
    #routerAddress("2")
    #routerAddress("3")
    print checkForUpdates("50", "121221230", -15, "1")
    print dict_storage
    print time_dict
    print checkForUpdates("50", "121221231", -32, "2")
    print dict_storage
    print checkForUpdates("50", "121221231", -24, "1")
    print dict_storage
    print checkForUpdates("50", "121221230", -12, "3")
    print dict_storage
    print checkForUpdates("50", "121221233", -15, "2")
    print dict_storage
    print checkForUpdates("50", "121221233", -24, "1")
    print checkForUpdates("50", "121221233", -55, "3")
    print dict_storage


