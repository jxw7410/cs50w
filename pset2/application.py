from classes import *
from threading import Lock


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
def disconnect():
    print(request.sid, " has disconnected")

@socketio.on("create_channel")
def create_channel(packet):
    channelname = packet["channel"]
    prev_channel = packet["prev_channel"]
    channel = Channel(channelname)
    try:
        app_channels.add_channel(channel)
    except app_channels.ChannelExistException:
        return emit("init_channel", {"channel" : False})
    #create room if not exist, and join it
    #roomname collision avoided due to code above
    user_id = request.sid
    leave_room(prev_channel, user_id)
    join_room(channelname, user_id)

    emit("init_channel", {"channel" : channelname}, room=channelname)


@socketio.on("join_channel")
def join_channel(packet):
    channelname = packet["channel"]
    prev_channel = packet["prev_channel"]
    if app_channels.is_channel(channelname):
        user_id = request.sid
        leave_room(prev_channel, user_id)
        join_room(channelname, user_id)
        return emit("joined_channel", {"request" : True})

    emit("joined_channel", {"request" : False})

@socketio.on("display_channels")
def display_channels():
    emit("display_channels", {"channels" : app_channels.display_channels()})

@socketio.on("send_message")
def message_send(packet):
    channelname = packet["channel"]
    message = packet["message"]
    if message:
        return emit("receive_message", {"confirm" : True, "message" : message}, room=channelname)
    emit("receive_message", {"confirm" : False})


if __name__ == "__main__":
    socketio.run(app, debug = True)