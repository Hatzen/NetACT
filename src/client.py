#!/usr/bin/env python
# encoding: utf-8
"""
Constants.py
"""

from socket import *
from subprocess import Popen, PIPE
import threading

from src import statics
from src import storage
from src import connection as con

# TODO: File location
file = "raw/file.java"


class Client:

    def __init__(self):
        self.process = None
        self.connection = None
        # https://stackoverflow.com/questions/22878625/receiving-broadcast-packets-in-python
        self.broadcast_socket = socket(AF_INET, SOCK_DGRAM)
        ip = storage.get(storage.KEY_SERVER_IP)
        port = storage.get(storage.KEY_BROADCAST_PORT)
        self.broadcast_socket.bind((ip, port))
        # Wait for new sessions in background
        thread = threading.Thread(target=self.receive_broadcast, args=())
        thread.daemon = True
        thread.start()

    def receive_broadcast(self):
        while True:
            # TODO: Refactore
            message = self.broadcast_socket.recvfrom(1024)
            print(message[0])

            tcp_socket = socket.socket()
            ip = storage.get(storage.KEY_SERVER_IP)
            port = storage.get(storage.KEY_SERVER_PORT)
            tcp_socket.connect((ip, port))
            # print('Got connection from ', (ip, port))
            self.connection = con.Connection(ip, port, tcp_socket)

    def execute_file(self):
        commands = []
        commands[0] = storage.get(storage.KEY_COMMAND_PART_I)
        commands[1] = storage.get(storage.KEY_FILE_NAME)
        commands[2] = storage.get(storage.KEY_COMMAND_PART_II)
        # TODO: CWD needed? FOR WORKING WITH FILE?
        self.process = Popen(commands, stdout=PIPE, stderr=PIPE, bufsize=1)

        # https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order
        threading.Thread(target=self.handle_error_stream, args=[self.process.stderr]).start()
        threading.Thread(target=self.handle_output_stream, args=[self.process.stdout]).start()

        # TODO: When end write back logfile with: stdout, stderr, exitcode, etc

    def handle_error_stream(self, stream):
        try:
            with stream:
                for line in iter(stream.readline, b''):
                    # TODO: Filter for "State" lines and send them to server.
                    print( line )
        finally:
            print( "Error" )

    def handle_output_stream(self, stream):
        try:
            with stream:
                for line in iter(stream.readline, b''):
                    print( line )
        finally:
            print( "Error" )


class ClientConnection(con.Connection):
    """
    A tcp Connection to a server.
    """

    def __init__(self, ip, port, sock):
        con.Connection.__init__(self, ip, port, sock)

    def handle_command(self, command):
        # Check for Commands, some may contain params
        if command == statics.COMMAND_SEND_FILE:
            filename = storage.get(storage.KEY_FILE_PATH)
            self.send_file(filename)
        elif command == statics.COMMAND_EXIT:
            self.sock.close()