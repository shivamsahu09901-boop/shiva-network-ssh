const WebSocket = require('ws');
const net = require('net');

const port = process.env.PORT || 10000;
const wss = new WebSocket.Server({ port: port, path: '/ws' }, () => {
    console.log(`WebSocket Tunnel running on port ${port} with path /ws`);
});

wss.on('connection', (ws, req) => {
    console.log('New connection attempt via WebSocket');
    const sshSocket = net.connect(22, '127.0.0.1', () => {
        console.log('Connected to internal SSH daemon');
    });

    ws.on('message', (message) => { sshSocket.write(message); });
    sshSocket.on('data', (data) => { if (ws.readyState === WebSocket.OPEN) ws.send(data); });
    ws.on('close', () => { sshSocket.end(); });
    sshSocket.on('close', () => { ws.close(); });
});
