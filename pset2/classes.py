from init_config import *

class Channel:
    #public variables
    #const static ref
    _size_limit_ = 100
    #stores channel name
    name = ""
    #stores up to 100 messages in channel
    messages = []
    #list of users relative to their username
    users={}

    def __init__(self, name):
        self.name = name
        self.users = {}
        self.messages=[]

    def add_message(self, message):
        if len(self.messages) == self._size_limit_:
            self.messages.pop(0)
            self.messages.append(message)
        else:
            self.messages.append(message)

    def add_user(self , name, prev_ch, sessionid):
        print("dictionary before add user", self.users)
        current_ch = self.name
        leave_room(prev_ch, sessionid)
        join_room(current_ch, sessionid)
        self.users[sessionid] = name

    def remove_user(self, sessionid):
        del self.users[sessionid]
        print("Remaining dictionary:", self.users)

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
        print("prev_channel is :", prev_channel)
        #store the initial user who created the channel to the new channel
        self.channels[new_channel.name].add_user(user_name, prev_channel, user_id)
        #remove the user from the previous channel
        try:
            self.channels[prev_channel].remove_user(user_id)
        except KeyError:
            pass
        #store or reassign the user_id with a reference to the active channel user is in
        self.users_ref[user_id] = new_channel.name

        #DEBUG
        try:
            print(self.channels[prev_channel].users)
        except KeyError:
            print("prev_channel is blank")


    #assign a user reference to indicate what channel the users are in
    def join_to_channel(self, channel_name, user_name, user_id):
        #if channel to join does not exist, raise exception
        if not channel_name in self.channels:
            raise self.ChannelNotExistException
        try:
            prev_channel = self.users_ref[user_id]
        except KeyError:
            prev_channel=""
        #add user to the other channel
        print("Previous Channel:", prev_channel)
        self.channels[channel_name].add_user(user_name, prev_channel,user_id)
        #remove the user from the previous channel
        try:
            self.channels[prev_channel].remove_user(user_id)
        except KeyError:
            pass
        #store or reassign the user_id with a reference to the active channel
        self.users_ref[user_id] = channel_name



    def disconnect_handler(self, user_id):
        #when connection is dropped, all references to channels are dropped
        try:
            channelname = self.users_ref[user_id]
            self.channels[channelname].remove_user(user_id)
            del self.users_ref[user_id]
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