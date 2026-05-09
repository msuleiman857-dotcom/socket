from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
# cors_allowed_origins="*" is important so browsers don't block the connection
socketio = SocketIO(app, cors_allowed_origins="*")

my_list = ["🍎 Apple", "🍌 Banana", "🍉 Watermelon", "🍇 Grapes", "🍓 Strawberry"]

def background_loop():
    """This function runs forever in the background"""
    while True:
        time.sleep(5)
        chosen_item = random.choice(my_list)
        print(f"Sending to frontend: {chosen_item}")
        socketio.emit('new_random_item', {'item': chosen_item})

@app.route('/')
def index():
    return render_template('index.html')

# We start the background task right before the first request or globally
socketio.start_background_task(background_loop)

if __name__ == '__main__':
    # This only runs locally. On Render, Gunicorn ignores this block.
    socketio.run(app, debug=True, port=5000)