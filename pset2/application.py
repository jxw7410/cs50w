from classes import *
from threading import Lock

class NoMessageError(Exception):
    pass

thread = None
thread_lock = Lock()

#Global Variable to store all generate channels
app_channels = Channels()

#not important, just testing something with multiple threads
def background_thread():
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response', {'data' : "Server generated event", 'count' : count})

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def test_connection():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    print(request.sid, " has connected")
    return emit('connection', {'data': 'Connected'})

@socketio.on('disconnect')
def ping_disconnect():
    print(request.sid, " has disconnected")

@socketio.on("create_channel")
def create_channel(packet):
    try:
        user = packet["user"]
        channelname = packet["channel"]
        if not user or not channelname:
            raise TypeError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : 100})
    except:
        return

    channelobj = Channel(channelname)
    try:
        app_channels.add_channel(channelobj)
        app_channels.channels[channelobj.name].add_user(request.sid, user, packet["prev_channel"], channelname)
    except app_channels.ChannelExistException:
        return emit("init_channel", {"channel" : False})

    emit("init_channel", {"channel" : channelname}, room=channelname)


@socketio.on("join_channel")
def join_channel(packet):
    try:
        user = packet["user"]
        channelname = packet["channel"]
        if not user or not channelname:
            raise TypeError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : -101})
    except:
        return emit("unknown_error")

    if app_channels.is_channel(channelname):
        app_channels.channels[channelname].add_user(request.sid, user, packet["prev_channel"], channelname)
        return emit("joined_channel", {"request" : True})

    emit("joined_channel", {"request" : False})

@socketio.on("display_channels")
def display_channels():
    emit("display_channels", {"channels" : app_channels.display_channels()})

@socketio.on("send_message")
def message_send(packet):
    try:
        channelname = packet["channel"]
        message = packet["message"]
        if channelname is None:
            raise TypeError
        if message is None:
            raise NoMessageError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : -102})
    except NoMessageError:
        return
    except:
        return emit("unknown_error")

    if request.sid in app_channels.channels[channelname].user:
        user = app_channels.channels[channelname].user[request.sid]
        return emit("receive_message", {"user": user, "confirm" : True, "message" : message}, room=channelname)



if __name__ == "__main__":
    socketio.run(app, debug = True)