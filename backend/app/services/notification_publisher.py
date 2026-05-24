import json
import asyncio
from uuid import UUID
import aioredis
from backend.app.config import settings

class NotificationPublisher:
    CHANNEL = 'notifications'

    def __init__(self):
        self.redis = None

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(settings.REDIS_URL, encoding='utf-8', decode_responses=True)

    async def publish(self, notification: dict):
        await self.connect()
        message = json.dumps(notification)
        await self.redis.publish(self.CHANNEL, message)

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None

notification_publisher = NotificationPublisher()
