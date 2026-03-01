javascript
(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('socket.io-client')) :
    typeof define === 'function' && define.amd ? define(['exports', 'socket.io-client'], factory) :
    (factory((global.io = {}),global.socketio));
}(this, (function (exports, socketio) { 'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var io = socketio;

return io;

})));
