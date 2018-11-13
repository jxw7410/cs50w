from init_config import *

class Channel:
    _size_limit_ = 100
    name = ""
    messages = []

    def __init__(self, name):
        self.name = name

    def add_message(self, message):
        if len(self.messages) == self._size_limit_:
            self.messages.pop(0)
            self.messages.append(message)
        else:
            self.messages.append(message)


class Channels:
    channels = {}

    def add_channel(self, Channel):
        if not Channel.name in self.channels:
            self.channels[Channel.name] = Channel
        else:
            raise Channels.ChannelExistException

    def display_channels(self):
        return [*channels]

    def add_message(self, Channel, message):
        self.channels[Channel].add_message(message)

    def is_channel(self, channel_name):
        if channel_name in self.channels:
            return True;
        return False;

    class ChannelExistException(Exception):
        pass

#Global Variable to store all generate channels
app_channels = Channels()


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def test_connection():
    return emit('my response', {'data': 'Connected'})

@socketio.on("Create Channel")
def create_channel(packet):
    channelname = packet["channel"]
    channel = Channel(channelname)
    try:
        app_channels.add_channel(channel)
    except app_channels.ChannelExistException:
        return emit("Initializing Channel", {"channel" : False})

    #create room if not exist, and join it
    #roomname collision avoided due to code above
    user_id = request.sid
    join_room(channelname, user_id)

    return emit("Initializing Channel", {"channel" : channelname}, room=channelname)


@socketio.on("Join Channel")
def join_channel(packet):
    channelname = packet["channel"]
    if app_channels.is_channel(channelname):
        user_id = request.sid
        join_room(channelname, user_id)
        return emit("Joining Channel", {"request" : True})
    return emit("Joining Channel", {"request" : False})

@socketio.on("Display Channels")
def display_channels():
    return emit("Displaying Channels", {"channels" : app_channels.display_channels()})

@socketio.on("Send Message")
def message_send(packet):
    channelname = packet["channel"]
    message = packet["message"]
    app_channels.add_message(channelname, message)
    return emit("Message Added", {"confirm" : True, "message" : message}, room=channelname)

if __name__ == "__main__":
    socketio.run(app)