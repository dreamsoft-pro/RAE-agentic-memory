import { Socket } from 'socket.io-client';

class SocketService {
  private mySocket: Socket;

  constructor(socket: Socket) {
    this.mySocket = socket;
  }

  public on(eventName: string, callback: (...args: any[]) => void): () => void {
    const _this = this;
    return this.mySocket.on(eventName, function (...args: any[]) {
      // Since we are in a Next.js environment and do not use Angular,
      // the $rootScope.$apply is replaced by ensuring that the callback
      // runs within the context of React or directly with DOM events.
      // This line can be removed if such behavior isn't necessary for your application.
      
      _this.mySocket.emit('event', 'data');  // Example emit, replace as needed

      callback.apply(_this.mySocket, args);
    });
  }
}

export default SocketService;