import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json



class WSHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    def open(self):
        self.write_message("Ack")
        self.connections.add(self)

    def on_close(self):
        self.connections.remove(self)

class DataHandler(tornado.web.RequestHandler):
    def post(self):
        mac = self.get_argument('mac')
        timestamp = self.get_argument('timestamp')
        signal = self.get_argument('signal_strength')
        router = self.get_argument('router')
        res = checkForUpdates(mac, timestamp, signal_strength, router_mac)
        if res:
            for socket in WSHandler.connections:
                socket.write_message(json.dumps({"mac":mac, "timestamp": timestamp, "signal":signal, "router": router}))


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r"/data", DataHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()


