import React from 'react';
import NotificationBell from './NotificationBell';

export default function Navbar() {
  return (
    <nav style={{ display: 'flex', alignItems: 'center', padding: '10px 20px', backgroundColor: '#fff', borderBottom: '1px solid #ddd' }}>
      <div style={{ flexGrow: 1 }}>
        <a href="/" style={{ fontWeight: 'bold', fontSize: '20px', color: '#333', textDecoration: 'none' }}>
          TaskFlow Pro
        </a>
      </div>
      <div style={{ position: 'relative' }}>
        <NotificationBell />
      </div>
    </nav>
  );
}
