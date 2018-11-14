#!/usr/bin/env python3
import codecs
import json
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
from itertools import dropwhile


NOT_FOUND = '''
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL /{path} was not found on this server.</p>
<hr>
<address>Garbage Server/0.0.1 at {host} Port {port}</address>
</body></html>
'''


def load_paths(path_file):
    paths = dict()
    with open(path_file, 'r') as f:
        for line in f:
            short, *full = map(lambda s: s.strip(), line.split(','))
            paths[short] = ''.join(full)

    return paths


def redirect_handler_class(port, path_file=os.getenv('REDIRECTS_FILE', './paths.txt')):
    class RedirectServerHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.host = 'buy-local'
            self.port = port
            self.path_file = path_file
            self.paths = load_paths(path_file)

            super(RedirectServerHandler, self).__init__(*args, **kwargs)
        
        def do_GET(self):
            # get rid of leading slashes
            path = ''.join(dropwhile(lambda c: c == '/', self.path))
            if path in self.paths.keys():
                self.send_response(302)
                self.send_header('Location', self.paths[path])
                self.end_headers()  # see base class
            else:
                self.send_headers(path='404.html', content_type='text/html', response=404)
                self.wfile.write(codecs.encode(
                    NOT_FOUND.format(path=path, host=self.host, port=self.port),
                    'ascii')
                )
                self.end_headers()  # see base class

        def send_headers(self, path, content_type, response=200):
            self.send_response(response)
            self.send_header('Content-type', content_type)
            self.end_headers()

    return RedirectServerHandler


if __name__ == '__main__':
    import socket
    import sys

    port = 8000
    if len(sys.argv) > 1:
        # PDF passes itself as first arg, so user command line args
        # will be +1 compared to normal
        port = int(sys.argv[1])
    address = ('', port)

    try:
        httpd = HTTPServer(address, redirect_handler_class(port))
        sa = httpd.socket.getsockname()
        sys.stdout.write(
            'Serving HTTP on {} port {} (http://{}:{}/) ...\n'.format(*(sa * 2))
        )
        httpd.serve_forever()
    except socket.error:
        sys.stderr.write(
            'Error opening socket for port {}.\n'
            'You can pass a different port to the server as an argument.\n'
            ''.format(port)  # mfw ''.format
        )
    except KeyboardInterrupt:
        sys.stderr.write(
            '\nKeyboard interrupt received, exiting.\n'
        )
    except Exception:
        sys.stderr.write(
            '\nLol, something broke.\n'
        )
        sys.exit(1)
