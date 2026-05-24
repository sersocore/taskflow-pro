import React from 'react';
import NotificationItem from './NotificationItem';

export default function NotificationDropdown({ notifications, onMarkAsRead }) {
  if (!notifications || notifications.length === 0) {
    return (
      <ul role="list" aria-label="Liste des notifications" style={{ padding: '8px', maxHeight: '300px', overflowY: 'auto' }}>
        <li style={{ padding: '8px', color: '#666' }}>Aucune notification</li>
      </ul>
    );
  }

  return (
    <div
      style={{
        position: 'absolute',
        right: 0,
        marginTop: '8px',
        width: '320px',
        maxHeight: '400px',
        overflowY: 'auto',
        backgroundColor: 'white',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        borderRadius: '4px',
        zIndex: 1000,
      }}
    >
      <ul role="list" aria-label="Liste des notifications" style={{ listStyle: 'none', margin: 0, padding: 0 }}>
        {notifications.slice(0, 20).map((n) => (
          <NotificationItem key={n.id} notification={n} onMarkAsRead={onMarkAsRead} />
        ))}
      </ul>
      <div style={{ padding: '8px', borderTop: '1px solid #eee', textAlign: 'center' }}>
        <button
          onClick={() => onMarkAsRead(notifications.filter(n => !n.read).map(n => n.id))}
          disabled={notifications.every(n => n.read)}
          style={{
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            padding: '8px 12px',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold',
          }}
          aria-disabled={notifications.every(n => n.read)}
        >
          Marquer tout comme lu
        </button>
      </div>
    </div>
  );
}
