import socketserver,

dict = {
        'a': 1,
        'b': 2
    }

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

        # while True:
        #     dt = datetime.now()

        #     #if True: #MyTCPHandler.new_time != last_time:
        #     #last_time = MyTCPHandler.new_time
        #     self.request.sendall(bytearray(str(dt), 'utf-8'))

        #     time.sleep(1.0)
        self.tempdata = list(self.data.split())
        if self.tempdata[0] == bytearray("give", 'utf-8'):
            try:
                if self.tempdata[1] == bytearray("all", 'utf-8'):
                    self.recvdata = list(dict.values())
                else:
                    self.recvdata = dict[self.tempdata[1].decode('utf-8')]
            except KeyError:
                self.recvdata = list(self.data.split())
        elif self.tempdata[0] == bytearray("change", 'utf-8'):
            if self.tempdata[1] == bytearray("a", 'utf-8'):
                dict['a'] = int(self.tempdata[2].decode('utf-8'))
                self.recvdata = "a is have changed"
            elif self.tempdata[1] == bytearray("b", 'utf-8'):
                dict['b'] = int(self.tempdata[2].decode('utf-8'))
                self.recvdata = "b is have changed"
        else:
            self.recvdata = list(self.data.split())
        #self.recvdata = "test"
        self.request.sendall(bytearray(str(self.recvdata), 'utf-8'))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__=='__main__':
    HOST = '127.0.0.1'    # The remote host
    PORT = 50016        # The same port as used by the server

    import sys
    if sys.argv[1] == 'client':
        # Echo client program
        import socket
       
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(bytearray(str(input()), 'utf-8'))
        # while True:
        #     data = s.recv(1024)
        #     print('Received', repr(data))
        data = s.recv(1024)
        print('Received', repr(data))
        s.close()
        
    else:

        # Create the server, binding to localhost on port 9999
        server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

