from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import host_info

PORT_NUMBER = 8080


# This class will handles any incoming request from
# the browser
class HttpHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        try:
            # Check the file extension required and
            # set the right mime type

            send_reply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                send_reply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                send_reply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                send_reply = True
            if self.path.endswith(".svg"):
                mimetype = 'image/svg+xml'
                send_reply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                send_reply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                send_reply = True

            if send_reply:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), HttpHandler)
    host_ip = host_info.ipaddress()
    print('Hosting HTTP server from ' + host_ip, PORT_NUMBER, sep=":")

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
