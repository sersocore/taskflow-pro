import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID
from backend.app.services.notification_service import NotificationService
from backend.app.services.notification_publisher import notification_publisher
from backend.app.db import get_db_pool

class TaskService:
    # Existing methods...

    @staticmethod
    async def assign_task(task_id: UUID, assigned_user_id: UUID, assigner_user_id: UUID):
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                # Update task assignment in DB
                await conn.execute('UPDATE tasks SET assigned_user_id = $1 WHERE id = $2', assigned_user_id, task_id)

                # Create notification content
                content = 'Nouvelle tâche assignée à vous.'

                # Create notification
                notification = await NotificationService.create_notification(
                    user_id=assigned_user_id,
                    content=content,
                    type='task_assignment',
                    task_id=task_id
                )

                # Publish notification event
                await notification_publisher.publish({
                    'id': str(notification.id),
                    'user_id': str(notification.user_id),
                    'content': notification.content,
                    'type': notification.type,
                    'task_id': str(notification.task_id) if notification.task_id else None,
                    'created_at': notification.created_at.isoformat(),
                    'read': notification.read
                })

    @staticmethod
    async def get_tasks_with_deadline_in_24h() -> List[dict]:
        pool = await get_db_pool()
        now = datetime.utcnow()
        target = now + timedelta(hours=24)
        query = '''
            SELECT id, assigned_user_id, deadline
            FROM tasks
            WHERE deadline >= $1 AND deadline <= $2
        '''
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, now, target)
            return [dict(row) for row in rows]

    @staticmethod
    async def create_deadline_reminder_notifications():
        tasks = await TaskService.get_tasks_with_deadline_in_24h()
        pool = await get_db_pool()
        for task in tasks:
            # Check if notification already exists for this task and type
            query_check = '''
                SELECT 1 FROM notifications
                WHERE task_id = $1 AND type = 'deadline_reminder' AND user_id = $2
                LIMIT 1
            '''
            async with pool.acquire() as conn:
                exists = await conn.fetchval(query_check, task['id'], task['assigned_user_id'])
                if exists:
                    continue

            content = 'Échéance de tâche dans moins de 24h.'
            notification = await NotificationService.create_notification(
                user_id=task['assigned_user_id'],
                content=content,
                type='deadline_reminder',
                task_id=task['id']
            )
            await notification_publisher.publish({
                'id': str(notification.id),
                'user_id': str(notification.user_id),
                'content': notification.content,
                'type': notification.type,
                'task_id': str(notification.task_id) if notification.task_id else None,
                'created_at': notification.created_at.isoformat(),
                'read': notification.read
            })
