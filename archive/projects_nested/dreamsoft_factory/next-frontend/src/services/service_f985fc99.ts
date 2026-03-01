import { useEffect, useRef } from 'react';
import api from '@/lib/api';

interface Order {
  ID: number;
  unreadMessages?: number;
}

const ChatComponent = ({ scope }: { scope: any }) => {
  const socketRef = useRef<SocketIOClient.Socket | null>(null);

  useEffect(() => {
    if (!socketRef.current) {
      socketRef.current = io('your-socket-url'); // Replace with actual URL
    }

    socketRef.current.on('connect', () => {
      console.log('Client has connected to the server!');
    });

    socketRef.current.emit('onOrdersPanel', { userID: scope.user.userID });

    socketRef.current.on('order.newMessage', (newMessage: any) => {
      const orderIdx = scope.orders.findIndex(order => order.ID === newMessage.orderID);
      if (orderIdx > -1 && !scope.orders[orderIdx].unreadMessages) {
        scope.orders[orderIdx] = {
          ...scope.orders[orderIdx],
          unreadMessages: 1
        };
      } else if (orderIdx > -1) {
        scope.orders[orderIdx] = {
          ...scope.orders[orderIdx],
          unreadMessages: scope.orders[orderIdx].unreadMessages + 1
        };
      }
    });

    return () => {
      socketRef.current?.off('connect');
      socketRef.current?.off('order.newMessage');
      // Clean up any other event listeners if necessary
    };
  }, [scope]);

  useEffect(() => {
    if (!socketRef.current) {
      socketRef.current = io('your-socket-url'); // Replace with actual URL
    }

    return () => {
      socketRef.current?.off('connect');
      // Clean up any other event listeners if necessary
    };
  }, []);

  return null; // ChatComponent doesn't render anything directly, but manages state and events.
};