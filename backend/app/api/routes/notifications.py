from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from backend.app.api.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.services.notification_service import NotificationService

router = APIRouter()

@router.get('/api/notifications')
async def get_notifications(current_user: User = Depends(get_current_user)):
    notifications = await NotificationService.get_recent_notifications(current_user.id)
    unread_count = await NotificationService.count_unread_notifications(current_user.id)
    return {
        'notifications': [
            {
                'id': str(n.id),
                'content': n.content,
                'created_at': n.created_at.isoformat(),
                'read': n.read,
                'type': n.type,
                'task_id': str(n.task_id) if n.task_id else None
            } for n in notifications
        ],
        'unread_count': unread_count
    }

@router.post('/api/notifications/mark-as-read')
async def mark_notifications_as_read(notification_ids: List[str], current_user: User = Depends(get_current_user)):
    try:
        uuids = [UUID(nid) for nid in notification_ids]
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid notification IDs')

    await NotificationService.mark_as_read(current_user.id, uuids)
    unread_count = await NotificationService.count_unread_notifications(current_user.id)
    return {'marked_as_read': notification_ids, 'unread_count': unread_count}
