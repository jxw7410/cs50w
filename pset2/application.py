from init_config import *

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("test data")
def test_func(packet):
     data = packet["data"]
     emit("Sending out data", {"data" : data}, broadcast = True)


if __name__ == "__main__":
    socketio.run(app)