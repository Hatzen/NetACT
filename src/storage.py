#!/usr/bin/env python
# encoding: utf-8
"""
Store config
"""

import configparser
from src import statics
from threading import Lock


# --Global Constants

# Both Keys
KEY_BROADCAST_PORT = "BROADCAST_PORT"
KEY_SERVER_PORT = "SERVER_PORT"
KEY_ROLE = "KEY_ROLE"

# Client Keys
KEY_CLIENT_ID = "CLIENT_ID"
KEY_SERVER_IP = "SERVER_IP"
KEY_COMMAND_PART_I = "COMMAND_PART_I"
KEY_FILE_NAME = "FILE_NAME"
KEY_COMMAND_PART_II = "COMMAND_PART_II"

# Server Keys
KEY_FILE_PATH = "FILE_PATH"

# Generated
KEY_SESSION_TOKEN = "SESSION_TOKEN"

# -- Vars
lock = Lock()
config = configparser.ConfigParser()
config.read(statics.CONFIG_FILE)


def get(key):
    lock.acquire()
    value = config[key]
    lock.release()
    return value


def put(key, value):
    config[key] = value
    config.write(statics.CONFIG_FILE)
    config.read(statics.CONFIG_FILE)
