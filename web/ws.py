import tornado.httpserver
import tornado.websocket
import tornado.ioloop 
import tornado.web
import json

from calc import checkForUpdates, position_routers, router1, router2, router3


router_macs = []
router_distances = []

class WSHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    def open(self):
        self.connections.add(self)
        if router1 and router2 and router3:
            socket.write_message(json.dumps(
                {'type': "routers", 
                'values': [
                    {'x': router1.x, 'y':router1.y}, 
                    {'x': router2.x, 'y': router2.y}, 
                    {'x': router3.x, 'y': router3.y}]}))

    def on_close(self):
        self.connections.remove(self)

class DeviceHandler(tornado.web.RequestHandler):
    def post(self):
        mac = self.get_argument('mac')
        timestamp = self.get_argument('timestamp')
        signal = self.get_argument('signal_strength')
        router = self.get_argument('router')
        res = checkForUpdates(mac, timestamp, int(signal), router)
        if res:
            x, y, mac = res
            for socket in WSHandler.connections:
                socket.write_message(json.dumps({"x": x, "y": y, "mac": mac, "type":device}))

class RouterHandler(tornado.web.RequestHandler):
    def post(self):
        # Arguments: 
        # [{mac: ..., signal: ..., to: ...},
        #  {mac: ..., signal: ..., to: ...}]
        if len(router_distances) < 6:
            args = json.loads(self.request.body)

            for distance in args:
                router_distances.append({'mac': distance['mac'], 'signal': distance['signal'], 'to': distance['to']})
            if len(router_distances) == 6:
                # sets some global variables in calc
                position_routers(router_distances)
                for socket in WSHandler.connections:
                    socket.write_message(json.dumps({'type': "routers", 'values': [{'x': router1.x, 'y':router1.y}, {'x': router2.x, 'y': router2.y}, {'x': router3.x, 'y': router3.y}]}))
            

class RouterHandshakeHandler(tornado.web.RequestHandler):
    def post(self):
        # Arguments
        # mac
        if len(router_macs) < 3:
            router = self.get_argument('mac')
            if not router in router_macs:
                router_macs.append(router)
    def get(self):
        self.write(json.dumps(router_macs))


class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        router_distances = []
        router_macs = []



application = tornado.web.Application([
    (r'/data/ws', WSHandler),
    (r'/data/device', DeviceHandler),
    (r'/data/router', RouterHandler),
    (r'/data/handshake', RouterHandshakeHandler),
    (r'/data/reset', ResetHandler)
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()


