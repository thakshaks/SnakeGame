import json
import time
import os
import redis
from tetris import TetrisGame

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")

r = redis.Redis(
    host=REDIS_HOST, 
    port=6379, 
    db=0,
    socket_timeout=10,
    socket_keepalive=True,
    health_check_interval=5
)

def run_game_loop(session_id):
    game = TetrisGame()
    pubsub = r.pubsub()
    pubsub.subscribe(f"input:{session_id}")
    
    # Broadcast initial state frame
    r.publish(f"state:{session_id}", json.dumps(game.get_state()))

    is_running = True
    while is_running:
        try:
            message = pubsub.get_message(ignore_subscribe_messages=True, timeout=0.01)
            if message and message['type'] == 'message':
                data = json.loads(message['data'].decode('utf-8'))
                action = data.get('action')
                if action == 'input':
                    game.handle_input(data.get('direction'))
                elif action == 'stop':
                    break
        except redis.exceptions.TimeoutError:
            pass

        state = game.update()
        r.publish(f"state:{session_id}", json.dumps(state))

        if state.get('game_over', False):
            break

        time.sleep(0.3)  # Tetris tick rate (300ms)

    try:
        pubsub.unsubscribe(f"input:{session_id}")
    except Exception:
        pass

def listen_for_sessions():
    pubsub = r.pubsub()
    pubsub.subscribe("control:tetris")
    print("Tetris Engine Microservice Listening...")

    while True:
        try:
            item = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if item and item['type'] == 'message':
                data = json.loads(item['data'].decode('utf-8'))
                if data.get('action') == 'start':
                    session_id = data.get('session_id')
                    run_game_loop(session_id)
        except redis.exceptions.TimeoutError:
            continue
        except Exception as e:
            print(f"Error in Tetris control listener: {e}")
            time.sleep(1)

if __name__ == '__main__':
    listen_for_sessions()