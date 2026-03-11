import api from '@/lib/api'; // Assuming this import statement follows some naming convention and not the actual axios

export default class SocketService {
    private ioSocket: any;
    private mySocket: any;

    constructor(private host: string, private port: number) {
        const socketUrl = `${this.host}:${this.port}`;
        this.ioSocket = io.connect(socketUrl);
        this.mySocket = socketFactory({ ioSocket: this.ioSocket, prefix: '' });
    }

    public emit(eventName: string, data: any): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.mySocket.emit(eventName, data, (response?: any) => resolve(response));
            } catch (error) {
                reject(error);
            }
        });
    }

    public broadcastEmit(eventName: string, data: any): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.mySocket.broadcast.emit(eventName, data, (response?: any) => resolve(response));
            } catch (error) {
                reject(error);
            }
        });
    }

    public removeListener(eventName: string): void {
        this.mySocket.removeListener(eventName);
    }
}