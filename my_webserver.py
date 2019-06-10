# Name: Chi Ho Leung
# PID:6106288
# 
# Reference: https://gist.github.com/MxShift/df19afcf0322ec7300b27f9d3b1e13fa
# Added audio/mp3, 'video/mp4 mime type extension.
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import path

hostName = "localhost"
hostPort = 8080

DIR_PATH = path.abspath(path.dirname(__file__))

validExtensions = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.json': 'application/json',
    '.mp3': 'audio/mp3',
    '.mp4': 'video/mp4',
    '.ico': 'image/vnd.microsoft.icon'
}


class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, file_path, mimeType):
        self.send_response(200)
        self.send_header('Content-Type', mimeType)
        self.send_header('Content-Length', path.getsize(file_path))
        self.end_headers()

    def _set_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        # self.send_header('Content-Length', '0')
        self.end_headers()
        self.wfile.write(bytes('<h1><center>404</center></h1>', 'utf-8'))

    def do_GET(self):
        file_path = self.getPath()
        mimeType = self.getMimeType(file_path)
        content = None

        if mimeType:
            content = self.getContent(file_path)

        if mimeType and content:
            self._set_headers(file_path, mimeType)
            self.wfile.write(content)
        else:
            self._set_404()

    def getMimeType(self, file_path):
        filename, file_extension = path.splitext(file_path)
        validMimeType = file_extension in validExtensions

        if validMimeType:
            return validExtensions[file_extension]
        else:
            print(
                'Invalid file extension: {ext} ("{req}")'
                .format(ext=file_extension, req=self.path)
            )

    def getPath(self):
        if self.path == '/':
            content_path = path.join(DIR_PATH, 'index.html')
        else:
            content_path = path.join(DIR_PATH, str(self.path)[1:])
        return content_path

    def getContent(self, content_path):
        file_exists = path.exists(content_path)

        if file_exists:
            with open(content_path, mode='r', encoding='utf-8') as f:
                content = f.read()
            print('Serving file: ', self.path)
            return bytes(content, 'utf-8')
        else:
            print('File not found: ', self.path)
        
myServer = HTTPServer((hostName, hostPort), RequestHandler)

try:
    print(
        '{time}:\nStarting web server at http://{host}:{port}'
        .format(time=time.asctime(), host=hostName, port=hostPort)
    )
    myServer.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    print(
        '{time}:\nStopping web server at http://{host}:{port}'
        .format(time=time.asctime(), host=hostName, port=hostPort)
    )    
myServer.server_close()
