#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

c200 = "HTTP/1.1 200 OK\r\n"
c301 = "HTTP/1.1 301 Moved Permanently\r\n"
c400 = "HTTP/1.1 400 Bad Request\r\n"
c404 = "HTTP/1.1 404 Not Found\r\n"
c405 = "HTTP/1.1 405 Method Not Allowed\r\n"


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.parse_request(self.data.decode("utf-8"))
        if self.path == "/" or self.path.endswith("/"):
            print("replaced")
            self.path +='index.html'
        if self.method != 'GET':
            self.request.sendall(bytearray(c405, 'utf-8'))
        if (self.method=='GET') & ('favicon.ico' not in self.path):
            self.do_GET()
    
    def do_GET(self):   
        self.path = "www%s" % self.path   
        try:  
            if not (self.path[-1] == "/" or self.path.endswith(".css") or self.path.endswith(".html")):
                self.path = (self.path).split('/')
                if 'www' not in self.path:
                    #print(path)
                    raise Exception
                else:
                    response = self.do_GET_301()
            else: 
                print("2nd")
                response = self.do_GET_200()
        except:
            response = c404
        finally:
            self.request.sendall(bytearray(response, 'utf-8'))
        print(self.path)
    

    def do_GET_301(self):
        response_head = c301 + "\nLocation: %s/\r\n" % self.path
        return response_head

    def do_GET_200(self):
        type =self.path.split(".")[1]
        print(type)
        with open(self.path, 'r') as file:
            data = file.read()
        response_head = c200 + "%" + "Content-Type: text/%s\r\n\r\n" % type + data
        return response_head 
        
    def parse_request(self, req):
        url = ''
        headers = {}
        lines = req.splitlines()
        inbody = False
        body = ''
        for line in lines[1:]:
            if 'Referer' in line:
                url = line.split(":",1)[1]
            if line.strip() == "":
                inbody = True
            if inbody:
                body += line
            else:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        method, path, _ = lines[0].split()
        self.path = path
        self.method = method
        self.headers = headers
        self.body = body
        print(url)
        try:
            self.path, self.query_string = self.path.split("?")
        except:
            pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    print("Server running")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    


"""GET / HTTP/1.1\r\n
Host: 127.0.0.1:8080\r\n
Connection: keep-alive\r\n
Cache-Control: max-age=0\r\n
sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"\r\n
sec-ch-ua-mobile: ?0\r\n
sec-ch-ua-platform:"Windows"\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36\r\n
 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n
 Sec-Fetch-Site: none\r\n
 Sec-Fetch-Mode: navigate\r\n
 Sec-Fetch-User: ?1\r\n
 Sec-Fetch-Dest: document\r\n
 Accept-Encoding: gzip, deflate, br\r\n
 Accept-Language: en-US,en;q=0.9'
 """