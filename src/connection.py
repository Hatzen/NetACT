
from threading import Thread
from src import statics

BUFFER_SIZE = 1024


class Connection(Thread):
    """
    A tcp Connection.
    """
    # http://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.run = True
        self.start()

    def run(self):
        while self.run:
            command = repr(self.sock.recv(BUFFER_SIZE))
            if command == statics.COMMAND_EXIT:
                self.run = False
            self.handle_command(command)

    # Have to be overriden
    def handle_command(self, command):
        pass

    def send_command(self, command, *params):
        for param in params:
            command += ":" + param
        self.sock.send(command)

    def send_file(self, file_path):
        with open(file_path, 'rb') as file:
            chunk = file.read(BUFFER_SIZE)
            while chunk:
                self.sock.send(chunk)
                chunk = file.read(BUFFER_SIZE)
            file.close()

    def receive_file(self, filename):
        with open(filename, 'wb') as file:
            chunk = self.sock.recv(BUFFER_SIZE)
            while chunk:
                file.write(chunk)
                chunk = self.sock.recv(BUFFER_SIZE)
            file.close()
