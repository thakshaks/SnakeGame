import json
import asyncio
import os
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.session_id = f"{self.game_name}_{id(self)}"
        
        await self.accept()
        self.redis = await aioredis.from_url(f"redis://{REDIS_HOST}:6379")
        self.listener_task = asyncio.create_task(self.listen_to_game_engine())

    async def disconnect(self, close_code):
        if hasattr(self, 'listener_task'):
            self.listener_task.cancel()
        if hasattr(self, 'redis'):
            await self.redis.publish(f"input:{self.session_id}", json.dumps({'action': 'stop'}))
            await self.redis.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))
            return

        elif action == 'start':
            # Dynamically route to control:snake or control:tetris
            control_channel = f"control:{self.game_name}"
            await self.redis.publish(control_channel, json.dumps({
                'action': 'start',
                'session_id': self.session_id
            }))

        elif action == 'input':
            await self.redis.publish(f"input:{self.session_id}", json.dumps({
                'action': 'input',
                'direction': data.get('direction')
            }))

    async def listen_to_game_engine(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"state:{self.session_id}")
        
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
                if message and message['type'] == 'message':
                    state_json = message['data'].decode('utf-8')
                    await self.send(text_data=state_json)
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Redis listener error: {e}")
        finally:
            await pubsub.unsubscribe(f"state:{self.session_id}")