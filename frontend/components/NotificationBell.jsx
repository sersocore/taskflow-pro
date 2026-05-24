import React from 'react';
import { useNotifications } from '../hooks/useNotifications';

export default function NotificationBell() {
  const { unreadCount, toggleDropdown } = useNotifications();

  return (
    <button
      aria-label="Notifications"
      aria-haspopup="true"
      aria-expanded="false"
      onClick={toggleDropdown}
      role="button"
      style={{
        position: 'relative',
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        padding: 0,
        margin: 0,
        outline: 'none',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        aria-hidden="true"
        width={24}
        height={24}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>
      {unreadCount > 0 && (
        <span
          aria-label={`${unreadCount} notifications non lues`}
          style={{
            position: 'absolute',
            top: 0,
            right: 0,
            backgroundColor: 'red',
            color: 'white',
            borderRadius: '50%',
            padding: '0 6px',
            fontSize: '12px',
            fontWeight: 'bold',
            lineHeight: '1',
            minWidth: '18px',
            textAlign: 'center',
            pointerEvents: 'none',
          }}
        >
          {unreadCount}
        </span>
      )}
    </button>
  );
}
