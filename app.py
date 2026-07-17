# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# Import your standalone game scripts
from games.snake import SnakeGame 

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Dictionary to track active games mapped to the user's WebSocket session ID
# Format: { "session_id": GameInstance }
active_games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f"Player connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    # Clean up memory when a player leaves
    if request.sid in active_games:
        del active_games[request.sid]

@socketio.on('start_game')
def handle_start_game(data):
    sid = request.sid
    game_choice = data.get('game')
    
    # Dynamically spin up the chosen game script
    if game_choice == 'snake':
        active_games[sid] = SnakeGame()
        emit('game_started', {'status': 'success', 'game': 'snake'})

@socketio.on('game_input')
def handle_game_input(data):
    sid = request.sid
    if sid in active_games:
        # Pass the input directly into the standalone game instance
        active_games[sid].handle_input(data)

# Centralized loop that updates ALL active games running on the server
def global_game_loop():
    while True:
        socketio.sleep(0.15) # Server tick rate
        
        # Iterate through every running game script and update it
        for sid, game_instance in list(active_games.items()):
            if not game_instance.get_state()['game_over']:
                game_instance.tick()
                # Send the state back strictly to the player running that game
                socketio.emit('game_update', game_instance.get_state(), to=sid)

if __name__ == '__main__':
    socketio.start_background_task(global_game_loop)
    socketio.run(app,host='0.0.0.0', debug=False)
    app.run('0.0.0.0',port=5000,threaded=False, debug=False)
