# 1. THIS MUST BE AT THE VERY TOP! It makes the server async-friendly.
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import random

app = Flask(__name__)
# 2. Explicitly tell SocketIO to use eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

my_list = ["🍎 Apple", "🍌 Banana", "🍉 Watermelon", "🍇 Grapes", "🍓 Strawberry"]

# Keep track of the background thread so we don't start 100 of them if 100 people connect
thread = None 

def background_loop():
    """This function runs forever in the background"""
    while True:
        socketio.sleep(5) # Must use socketio.sleep!
        chosen_item = random.choice(my_list)
        print(f"Sending to frontend: {chosen_item}")
        socketio.emit('new_random_item', {'item': chosen_item})

@app.route('/')
def index():
    return render_template('index.html')

# 3. THE FIX: Only start the loop AFTER the server is booted and a user connects
@socketio.on('connect')
def handle_connect():
    global thread
    print("A user connected!")
    if thread is None:
        print("Starting the background loop for the first time...")
        thread = socketio.start_background_task(background_loop)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
