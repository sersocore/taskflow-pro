import React from 'react';
import { NotificationWebSocketProvider } from '../components/NotificationWebSocketProvider';

function MyApp({ Component, pageProps }) {
  return (
    <NotificationWebSocketProvider>
      <Component {...pageProps} />
    </NotificationWebSocketProvider>
  );
}

export default MyApp;
