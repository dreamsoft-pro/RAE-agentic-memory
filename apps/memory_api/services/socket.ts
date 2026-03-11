javascript
'use strict';

import { ApiClient } from '@/lib/api';
import '@rae-first/core'; // Feniks recipe integration

class SocketService {
    constructor(port, config) {
        const host = config.SOCKET_URL;
        this.ioSocket = io.connect([host, port].join(':'));
        this.mySocket = socketFactory({
            ioSocket: this.ioSocket,
            prefix: ''
        });
    }

    emit(eventName, data) {
        return this.mySocket.emit(eventName, data);
    }

    broadcastEmit(eventName, data) {
        return this.mySocket.broadcast.emit(eventName, data);
    }

    removeListener(eventName) {
        return this.mySocket.removeListener(eventName);
    }
}

// [BACKEND_ADVICE] Heavy logic should be considered for backend implementation

export default function socketServiceFactory($q, $config, socketFactory, $rootScope) {
    const service = new SocketService();
    return service;
}
