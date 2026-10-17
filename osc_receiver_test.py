"""
Receptor OSC de prueba — corre en tu máquina con el software de música
=======================================================================
Instala dependencias:
    pip install python-osc

Uso:
    python3 osc_receiver_test.py

Muestra los datos de acelerómetro en tiempo real.
Adapta handle_accel() para conectar con tu software musical.
"""

from pythonosc import dispatcher, osc_server
import argparse, math

LISTEN_IP   = "0.0.0.0"   # escucha en todas las interfaces
LISTEN_PORT = 5005

def handle_accel(address, x, y, z, mag):
    # ── Aquí conectas con tu software de música ──────────────────────────
    # Ejemplo: mapear magnitud a volumen, eje X a pitch, etc.
    # Si usas SuperCollider, esto lo hace directamente NetAddr.
    # Si usas Max/MSP o Pd, configura udpreceive al puerto 5005.
    # ─────────────────────────────────────────────────────────────────────
    bar = "█" * int(mag * 5)
    print(f"x:{x:+.3f}  y:{y:+.3f}  z:{z:+.3f}  |g|:{mag:.3f}  {bar}")

if __name__ == "__main__":
    d = dispatcher.Dispatcher()
    d.map("/accel", handle_accel)

    server = osc_server.ThreadingOSCUDPServer((LISTEN_IP, LISTEN_PORT), d)
    print(f"Escuchando OSC en {LISTEN_IP}:{LISTEN_PORT} ...")
    print("Ctrl+C para salir\n")
    server.serve_forever()
