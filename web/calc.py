
#holds device MAC addresses, dictionary of timestamps, and signal strengths 
dict_storage = {}
#holds MAC addresses, timestamps, and final (x,y) coordinates; dict_coord[mac][n] where n = 0(timestamp), 1(x coord), 2(y coord)
dict_coordinates = []
#holds router MAC Addresses, should hold 3 values max
router_addresses = {}

def routerAddress(router_mac_addr) :

	i = 0
	while (len(router_addresses.keys()) < 4 and (i < 3)) :
		if (not router_addresses.has_key(router_mac_addr)) :
			router_addresses[router_mac_addr] = i
			i += 1
	

def checkForUpdates(mac_addr, timestamp, signal, router_addr):


	if (not dict_storage.has_key(mac_addr)):
		dict_storage[mac_addr] = {timestamp: {0, 0, 0}}	
		dict_coordinates.append(mac_addr)
		dict_coordinates[mac_addr] = {}
	if (not dict_storage[mac_addr].has_key[timestamp]) :
		dict_storage[mac_addr][timestamp] = {0, 0, 0}
	dict_storage[mac_addr][timestamp][router_addresses[router_addr]] = signal
	for x in dict_storage[mac_addr][timestamp]:
		if x == 0 :
			return None
	if timestamp > dict_coordinates[mac_addr][0] :
		dict_coordinates[mac_addr][0] = timestamp
		dict_coordinates[mac_addr][1] = trilateration_x(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][1])
		dict_coordinates[mac_addr][2] = trilateration_y(dict_storage[mac_addr][timestamp][0], dict_storage[mac_addr][timestamp][2], dict_coordinates[mac_addr][1])
		del dict_storage[mac_addr][timestamp]
		return (dict_coordinates[mac_addr][1], dict_coordinates[mac_addr][2], mac_addr) #returns (x, y, MAC addr) as tuple
	else: 
		del dict_storage[mac_addr][timestamp]
		return None


def sig_strengthToDistance(signal_strength) :

	distance = (27.55 - 20*(math.log10(2437) + math.fabs(signal_strength)) / 20
	distance = math.pow(10.0, distance)
	return distance

def trilateration_x(s1, s2) :

	x = (math.pow(s1, 2) - math.pow(s2, 2) + math.pow(x2, 2)) / (2 * x2)
	return x

def trilateration_y(s1, s3, trilat_x) :

	y = ((math.pow(s1, 2) - math.pow(s3, 2) + math.pow(x3, 2) + math.pow(y3, 2)) / (2 * y3)) - ((x3 * trilat_x) / y3)
	return y



