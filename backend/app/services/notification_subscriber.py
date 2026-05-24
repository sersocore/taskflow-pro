import asyncio
import json
import aioredis
from backend.app.services.websocket_manager import websocket_manager
from backend.app.config import settings

class NotificationSubscriber:
    CHANNEL = 'notifications'

    def __init__(self):
        self.redis = None
        self.task = None

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(settings.REDIS_URL, encoding='utf-8', decode_responses=True)

    async def start(self):
        await self.connect()
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.CHANNEL)

        async def reader():
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        user_id = data.get('user_id')
                        if user_id:
                            await websocket_manager.broadcast_to_user(user_id, data)
                    except Exception as e:
                        # Log error
                        print(f"Error processing notification message: {e}")

        self.task = asyncio.create_task(reader())

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        if self.redis:
            await self.redis.close()
            self.redis = None

notification_subscriber = NotificationSubscriber()
