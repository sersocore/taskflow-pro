import asyncio
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from asyncpg import Connection
from backend.app.db import get_db_pool
from backend.app.models.notification import Notification

class NotificationService:
    @staticmethod
    async def create_notification(user_id: UUID, content: str, type: str, task_id: Optional[UUID] = None) -> Notification:
        query = '''
            INSERT INTO notifications (user_id, content, type, task_id, created_at, read)
            VALUES ($1, $2, $3, $4, now(), false)
            RETURNING id, user_id, content, type, task_id, created_at, read
        '''
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id, content, type, task_id)
            notification = Notification(
                id=row['id'],
                user_id=row['user_id'],
                content=row['content'],
                type=row['type'],
                task_id=row['task_id'],
                created_at=row['created_at'],
                read=row['read']
            )
            return notification

    @staticmethod
    async def get_recent_notifications(user_id: UUID, limit: int = 20) -> List[Notification]:
        query = '''
            SELECT id, user_id, content, type, task_id, created_at, read
            FROM notifications
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        '''
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, user_id, limit)
            notifications = [Notification(
                id=row['id'],
                user_id=row['user_id'],
                content=row['content'],
                type=row['type'],
                task_id=row['task_id'],
                created_at=row['created_at'],
                read=row['read']
            ) for row in rows]
            return notifications

    @staticmethod
    async def count_unread_notifications(user_id: UUID) -> int:
        query = '''
            SELECT COUNT(*) FROM notifications WHERE user_id = $1 AND read = false
        '''
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            count = await conn.fetchval(query, user_id)
            return count

    @staticmethod
    async def mark_as_read(user_id: UUID, notification_ids: List[UUID]) -> None:
        if not notification_ids:
            return
        query = '''
            UPDATE notifications
            SET read = true
            WHERE user_id = $1 AND id = ANY($2::uuid[])
        '''
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, user_id, notification_ids)
