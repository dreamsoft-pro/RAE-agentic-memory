/**
 * Service: socket
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import io from 'socket.io-client';
import { useEffect, useState } from 'react';
import { useConfig } from './configContext'; // Assuming you have a config context for $config

const SocketService = () => {
    const [mySocket, setMySocket] = useState<any>(null);
    const config = useConfig();

    useEffect(() => {
        if (config && config.SOCKET_URL) {
            const host = config.SOCKET_URL;
            const ioSocket = io([host]);
            setMySocket(ioSocket);
        }
    }, [config]);

    const emit = (eventName: string, data: any) => {
        if (mySocket) {
            mySocket.emit(eventName, data);
        }
    };

    const broadcastEmit = (eventName: string, data: any) => {
        if (mySocket) {
            mySocket.broadcast.emit(eventName, data);
        }
    };

    const remove = (eventName: string) => {
        if (mySocket) {
            mySocket.removeListener(eventName);
        }
    };

    const on = (eventName: string, callback: Function) => {
        if (mySocket) {
            mySocket.on(eventName, (...args: any[]) => {
                callback(...args);
            });
        }
    };

    return { emit, broadcastEmit, remove, on };
};

export default SocketService;

This code is a modernized version of your legacy AngularJS service adapted for use in a React/TypeScript environment. It uses hooks like `useEffect` and `useState` to manage the socket connection and its methods. The configuration is assumed to be provided via a context (`useConfig`), which you'll need to implement based on your application structure.