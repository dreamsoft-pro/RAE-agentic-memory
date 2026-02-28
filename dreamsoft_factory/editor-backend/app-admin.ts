import 'reflect-metadata';
import express from 'express';
import {Db, MongoClient} from "mongodb";
import {Packet, Socket} from "socket.io";
import {createSocketServer, useSocketServer} from "socket-controllers";

import {importClassesFromDirectories} from "socket-controllers/util/DirectoryExportedClassesLoader";
import {controllers} from "./controllers2";

const app = express();
const PORT = (process.env.PORT || 3000) as number;
// app.set("port", PORT);

const http = require("http").Server(app);
const server = http.listen(PORT, () => {
    console.log(`listening on *:${PORT}`);
});
const io = require("socket.io")(server);
const mainConf = require('./confs/main');
const companyID = mainConf.companyID;
const  databaseName = 'editor_' + companyID;
const mongoClient = new MongoClient("mongodb://" + mainConf.mongoUser + ":" + mainConf.mongoPwd + "@" + mainConf.mongoHost + ":" + mainConf.mongoPort + "/" + databaseName + "?authSource=admin");
export let mongoDb:Db;
mongoClient.connect().then(()=>{
mongoDb = mongoClient.db(databaseName)
});
io.on("connection", (socket: any) => {
    socket.use((packet: Packet, next: (err?: any) => void) => {
        const [controller, method] = packet[0].split('.');
        const instance = new (<any>controllers)[controller](socket, mongoClient);
        instance[method](packet[1]);
        next();
    });
});

