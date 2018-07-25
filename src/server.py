#!/usr/bin/env python
# encoding: utf-8
"""
Constants.py
"""

from socket import *
from threading import Thread

import string
import random

from src import statics
from src import storage
from src import connection as con


class Server:

    def __init__(self):
        self.connections = []
        self.session_token = None
        # Init broadcast socket for sending
        self.broadcast_socket = socket(AF_INET, SOCK_DGRAM)
        # Init tcp socket for listening for clients to connect
        self.tcp_socket = socket.socket()
        port = storage.get(storage.KEY_SERVER_PORT)
        self.tcp_socket.bind((socket.gethostname(), port))
        # Wait for connections in background
        thread = Thread(target=self.listen_for_clients, args=())
        thread.daemon = True
        thread.start()
        # When server is started release file
        self.release_file()

    def release_file(self):
        self.create_session_token()
        self.send_broadcast()

    def create_session_token(self):
        """
        Create a unique string so every client will
        notice which session should be running now
        """
        self.session_token = storage.get(storage.KEY_SESSION_TOKEN)
        if self.session_token == "":
            self.session_token = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.session_token = hash(self.session_token)
        storage.put(storage.KEY_SESSION_TOKEN, self.session_token)

    def send_broadcast(self):
        """
        Notify all clients via broadcast to start a new session
        """
        # https://stackoverflow.com/questions/22878625/receiving-broadcast-packets-in-python
        self.broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        port = storage.get(storage.KEY_BROADCAST_PORT)
        message = statics.COMMAND_NEW_SESSION + self.session_token
        self.broadcast_socket.sendto(message, ('255.255.255.255', port))

    def listen_for_clients(self):
        self.tcp_socket.listen(5)
        print('Server listening....')
        while True:
            (conn, (ip, port)) = self.tcp_socket.accept()
            # print('Got connection from ', (ip, port))
            connection = con.Connection(ip, port, conn)
            self.connections.append(connection)


class ServerConnection(con.Connection):
    """
    A tcp Connection to a client.
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