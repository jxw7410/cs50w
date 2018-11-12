from init_config import *

class Channel:
    _size_limit_ = 100
    name = ""
    messages = []

    def __init__(self, name):
        self.name = name

    def add_message(self, message):
        if len(messages) == _size_limit_:
            messages.pop(0)
            messages.append(message)
        else:
            messages.append(message)


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
    name = packet["name"]
    channel = Channel(name)
    try:
        app_channels.add_channel(channel)
    except app_channels.ChannelExistException:
        return emit("Initializing Channel", {"channel" : False})

    #create room if not exist, and join it
    #roomname collision avoided due to code above
    user_id = request.sid
    join_room(name, user_id)

    return emit("Initializing Channel", {"channel" : name}, room=name)




@socketio.on("Display Channels")
def display_channels():
    return emit("Displaying Channels", {"channels" : app_channels.display_channels()})

@socketio.on("Message Append")
def message_append(packet):
    name = packet["name"]
    message = packet["message"]
    app_channels.add_message(name, message)
    return emit("Message Added", {"data" : [name, message]}, room=name)

if __name__ == "__main__":
    socketio.run(app)