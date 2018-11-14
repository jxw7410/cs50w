from init_config import *

class Channel:
    _size_limit_ = 100
    name = ""
    messages = []
    user={}

    def __init__(self, name):
        self.name = name

    def add_message(self, message):
        if len(self.messages) == self._size_limit_:
            self.messages.pop(0)
            self.messages.append(message)
        else:
            self.messages.append(message)

    def add_user(self, sessionid, name, prev_ch, current_ch):
        leave_room(prev_ch, sessionid)
        join_room(current_ch, sessionid)
        self.user[sessionid] = name

class Channels:
    channels = {}

    #register a Channel object to Channels under Channel name as the key
    def add_channel(self, Channel):
        if not Channel.name in self.channels:
            self.channels[Channel.name] = Channel
        else:
            raise Channels.ChannelExistException

    def display_channels(self):
        return [*(self.channels)]

    def add_message(self, Channel, message):
        self.channels[Channel].add_message(message)

    def is_channel(self, channel_name):
        if channel_name in self.channels:
            return True;
        return False;

    class ChannelExistException(Exception):
        pass