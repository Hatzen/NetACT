#!/usr/bin/env python
# encoding: utf-8
"""
Constants.py
"""

MESSAGE_PREFIX = "**//**NetACTCommunicator**START**"
MESSAGE_POSTFIX = "**END**NetACTCommunicator**//**"

CONFIG_FILE = "config.ini"
PROGRAM_PATH = "raw/tmp/"


COMMAND_NEW_SESSION = "COMMAND_NEW_SESSION"
COMMAND_SEND_FILE = "COMMAND_SEND_FILE"
COMMAND_UPDATE_STATE = "COMMAND_UPDATE_STATE"  # Client appends Param: ClientId, State
COMMAND_EXIT = "COMMAND_EXIT"
