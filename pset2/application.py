from classes import *


class NoMessageError(Exception):
    pass



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
    app_channels.disconnect_handler(request.sid)
    print(request.sid, " has disconnected")

@socketio.on("create_channel")
def create_channel(packet):
    try:
        user = packet["user"]
        channel_name = packet["channel"]
        if not user or not channel_name:
            raise TypeError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : 100})

    try:
        app_channels.add_channel(channel_name, user, request.sid)
    except app_channels.ChannelExistException:
        return emit("init_channel", {"channel" : False})

    emit("init_channel", {"channel" : channel_name}, room=channel_name)


@socketio.on("join_channel")
def join_channel(packet):
    try:
        user = packet["user"]
        channel_name = packet["channel"]
        if not user or not channel_name:
            raise TypeError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : -101})

    try:
        print("before join", app_channels.users_ref)
        app_channels.join_to_channel(channel_name, user, request.sid)
        print("after join", app_channels.users_ref)
    except app_channels.ChannelNotExistException:
        return emit("joined_channel", {"request" : False})

    emit("joined_channel", {"request" : True})

@socketio.on("display_channels")
def display_channels():
    emit("display_channels", {"channels" : app_channels.display_channels()})

@socketio.on("send_message")
def message_send(packet):
    try:
        message = packet["message"]
        if message is "":
            raise NoMessageError
    except TypeError:
        return emit("missing_arg_error", {"errorcode" : -102})
    except NoMessageError:
        return
    except:
        return emit("unknown_error")

    channelname = app_channels.users_ref[request.sid]
    channel = app_channels.channels[channelname]

    print(channel.last_request.request_id == request.sid)

    if channel.last_request.request_id == request.sid and not channel.last_request.is_minute():
        merge = True
    else:
        merge = False

    channel.last_request.time = time.time()
    channel.last_request.request_id = request.sid

    if request.sid in channel.users:
        user = channel.users[request.sid]
        return emit("receive_message", {"user": user, "confirm" : True, "message" : message, "merge" : merge}, room=channelname)



if __name__ == "__main__":
    socketio.run(app, debug = True)