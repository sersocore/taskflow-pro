import React from 'react';

export default function NotificationItem({ notification, onMarkAsRead }) {
  const { id, content, created_at, read, type } = notification;

  const handleClick = () => {
    if (!read) {
      onMarkAsRead([id]);
    }
  };

  const date = new Date(created_at);
  const formattedDate = date.toLocaleString();

  return (
    <li
      role="listitem"
      onClick={handleClick}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      }}
      style={{
        padding: '10px 12px',
        cursor: 'pointer',
        backgroundColor: read ? 'white' : '#e6f7ff',
        borderBottom: '1px solid #eee',
        fontWeight: read ? 'normal' : 'bold',
        outline: 'none',
      }}
      aria-pressed={read}
      aria-label={`${content} - ${formattedDate} - ${read ? 'Lu' : 'Non lu'}`}
    >
      <div style={{ fontSize: '14px', marginBottom: '4px' }}>{content}</div>
      <div style={{ fontSize: '12px', color: '#999' }}>{formattedDate}</div>
    </li>
  );
}
