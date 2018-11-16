from init_config import *
import time

class Channel:
    #public variables
    #const static ref
    _size_limit_ = 100

    def __init__(self, name):
        #stores channel name
        self.name = name
        #list of users relative to their username
        self.users = {}
        #stores up to 100 messages in channel
        self.messages=[]
        #stores instance of last request
        self.last_request = self.Last_Request()

    def add_message(self, message):
        if len(self.messages) == self._size_limit_:
            self.messages.pop(0)
            self.messages.append(message)
        else:
            self.messages.append(message)

    def add_user(self , name, prev_ch, sessionid):
        current_ch = self.name
        leave_room(prev_ch, sessionid)
        join_room(current_ch, sessionid)
        self.users[sessionid] = name

    def remove_user(self, sessionid):
        del self.users[sessionid]

    class Last_Request:
        time = 0
        request_id = ""
        def is_minute(self):
            self.time = int(time.time() - self.time)
            print(self.time)
            if self.time >= 60:
                return True
            return False

class Channels:
    #public variables
    #stores dictionary of channels
    channels = {}
    #stores references of active users to a particular channel
    users_ref = {}
    #register a Channel object to Channels under Channel name as the key
    def add_channel(self, channel_name, user_name, user_id):
        #if channel already exists, raise exception
        if channel_name in self.channels:
            raise self.ChannelExistException
        #create a channel
        new_channel = Channel(channel_name)
        #store new channel indexed by it's name as the key
        self.channels[new_channel.name] = new_channel
        try:
            prev_channel = self.users_ref[user_id]
        except KeyError:
            prev_channel = ""
        #store the initial user who created the channel to the new channel
        self.channels[new_channel.name].add_user(user_name, prev_channel, user_id)
        #remove the user from the previous channel
        try:
            self.channels[prev_channel].remove_user(user_id)
        except KeyError:
            pass
        #store or reassign the user_id with a reference to the active channel user is in
        self.users_ref[user_id] = new_channel.name


    #assign a user reference to indicate what channel the users are in
    def join_to_channel(self, channel_name, user_name, user_id):
        #if channel to join does not exist, raise exception
        if not channel_name in self.channels:
            raise self.ChannelNotExistException

        try:
            prev_channel = self.users_ref[user_id]
        except KeyError:
            print("error 701: KeyError of Prev Channel")
            prev_channel=""
        #add user to the other channel

        self.channels[channel_name].add_user(user_name, prev_channel,user_id)
        #remove the user from the previous channel
        try:
            self.channels[prev_channel].remove_user(user_id)
        except KeyError:
            print("error 702: KeyError of Removing User from Prec Channel")
            pass
        #store or reassign the user_id with a reference to the active channel
        self.users_ref[user_id] = channel_name



    def disconnect_handler(self, user_id):
        #when connection is dropped, all references to channels are dropped
        try:
            channelname = self.users_ref[user_id]
            self.channels[channelname].remove_user(user_id)
            del self.users_ref[user_id]
            print(self.users_ref)
        except KeyError:
            pass

    def display_channels(self):
        return [*(self.channels)]

    def add_message(self, channel_name, message):
        self.channels[channel_name].add_message(message)

    def is_channel(self, channel_name):
        if channel_name in self.channels:
            return True;
        return False;

    class ChannelExistException(Exception):
        pass

    class ChannelNotExistException(Exception):
        pass

#init global instance of my class
app_channels = Channels()

