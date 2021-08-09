from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import parse_headers
import urllib.parse as urlparse
from urllib.parse import parse_qs
from shlex import quote
import re
import logging
import subprocess
import cgi
import win32event, win32api, winerror

cmdRegex = re.compile(r'choco install ([a-zA-Z0-9_\-]+)')

class ChocolateyLauncher(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        queries = parse_qs(parsed.query)
        cmdQuery = queries.get('cmd', [None])[0]

        if cmdQuery and cmdRegex.match(cmdQuery):
            referrer = self.headers.get('Referer', None)
            if not referrer or referrer != 'https://community.chocolatey.org/':
                logging.error('Invalid referrer %s' % referrer)
                return

            cmd = "start /b powershell -Command \"Start-Process cmd -Verb RunAs -ArgumentList '/c %s'\"" % cmdQuery
            logging.info(cmd)
            subprocess.call(cmd, shell=True)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("OK", "utf-8"))
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Bad params", "utf-8"))

def run(server_class=HTTPServer, handler_class=ChocolateyLauncher, port=22567):
    logging.basicConfig(level=logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    mutex = win32event.CreateMutex(None, 1, "cqinst")
    lasterror = win32api.GetLastError()
    if lasterror == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        raise RuntimeError("Single instance only allowed")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
