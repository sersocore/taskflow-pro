import { useState, useEffect, useCallback, useRef } from 'react';

export function useNotifications() {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const fetchNotifications = useCallback(async () => {
    try {
      const res = await fetch('/api/notifications', { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        setNotifications(data.notifications);
        setUnreadCount(data.unread_count);
      }
    } catch (error) {
      console.error('Failed to fetch notifications', error);
    }
  }, []);

  const markAsRead = useCallback(async (ids) => {
    if (!ids || ids.length === 0) return;
    try {
      const res = await fetch('/api/notifications/mark-as-read', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ notification_ids: ids }),
      });
      if (res.ok) {
        const data = await res.json();
        setNotifications((prev) =>
          prev.map((n) => (ids.includes(n.id) ? { ...n, read: true } : n))
        );
        setUnreadCount(data.unread_count);
      }
    } catch (error) {
      console.error('Failed to mark notifications as read', error);
    }
  }, []);

  const connectWebSocket = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${protocol}://${window.location.host}/ws/notifications`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      // console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data && data.id) {
          setNotifications((prev) => {
            const exists = prev.find((n) => n.id === data.id);
            if (exists) return prev;
            const newList = [data, ...prev];
            if (newList.length > 20) newList.pop();
            return newList;
          });
          setUnreadCount((count) => count + 1);
        }
      } catch (e) {
        console.error('Error parsing WebSocket message', e);
      }
    };

    ws.onclose = () => {
      // console.log('WebSocket disconnected, retrying in 5s');
      reconnectTimeoutRef.current = setTimeout(() => {
        connectWebSocket();
      }, 5000);
    };

    ws.onerror = (err) => {
      console.error('WebSocket error', err);
      ws.close();
    };
  }, []);

  useEffect(() => {
    fetchNotifications();
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [fetchNotifications, connectWebSocket]);

  const toggleDropdown = () => setDropdownOpen((o) => !o);

  return { notifications, unreadCount, dropdownOpen, fetchNotifications, markAsRead, toggleDropdown };
}
