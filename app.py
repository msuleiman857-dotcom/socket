from flask import Flask, render_template
from flask_socketio import SocketIO
import random
# 1. We no longer need 'import time'

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

my_list = ["🍎 Apple", "🍌 Banana", "🍉 Watermelon", "🍇 Grapes", "🍓 Strawberry"]

def background_loop():
    """This function runs forever in the background"""
    while True:
        # 2. THE FIX: Use socketio.sleep instead of time.sleep
        socketio.sleep(5) 
        
        chosen_item = random.choice(my_list)
        print(f"Sending to frontend: {chosen_item}")
        socketio.emit('new_random_item', {'item': chosen_item})

@app.route('/')
def index():
    return render_template('index.html')

socketio.start_background_task(background_loop)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
