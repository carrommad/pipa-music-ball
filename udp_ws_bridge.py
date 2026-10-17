"""
Bridge UDP → WebSocket
======================
Recibe paquetes del Atom S3 por UDP (puerto 5005)
y los reenvía al navegador por WebSocket (puerto 8765).

Instalar:
    pip install websockets

Uso:
    python3 udp_ws_bridge.py
    Luego abre visualizer.html en el navegador.
"""

import asyncio
import socket
import struct
import json
import websockets
from websockets.server import serve

UDP_PORT = 5005
WS_PORT  = 8765

clients = set()

async def ws_handler(websocket):
    clients.add(websocket)
    print(f"Browser conectado ({len(clients)} clientes)")
    try:
        await websocket.wait_closed()
    finally:
        clients.discard(websocket)
        print(f"Browser desconectado ({len(clients)} clientes)")

async def udp_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    sock.setblocking(False)
    loop = asyncio.get_event_loop()
    print(f"Escuchando UDP en puerto {UDP_PORT}...")

    while True:
        try:
            data = await loop.run_in_executor(None, sock.recv, 16)
            if len(data) == 16:
                x, y, z, mag = struct.unpack('<ffff', data)
                msg = json.dumps({"x": round(x,4), "y": round(y,4),
                                  "z": round(z,4), "mag": round(mag,4)})
                if clients:
                    await asyncio.gather(
                        *[c.send(msg) for c in list(clients)],
                        return_exceptions=True
                    )
        except Exception as e:
            await asyncio.sleep(0.001)

async def main():
    print(f"WebSocket en ws://localhost:{WS_PORT}")
    async with serve(ws_handler, "0.0.0.0", WS_PORT):
        await udp_loop()

asyncio.run(main())
