# Pipa-Music-Ball — Bio-Kinetic Interactive Instrument & Telemetry

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Hardware: M5Stack Atom S3](https://img.shields.io/badge/Hardware-M5Stack%20Atom%20S3-orange.svg)](https://docs.m5stack.com/en/core/AtomS3)
[![IMU: MPU6886](https://img.shields.io/badge/IMU-6--DoF%20MPU6886-teal.svg)]()

An embedded bio-kinetic physical computing instrument housed inside an interactive rolling sphere. 
Powered by an **M5Stack Atom S3** (ESP32-S3 microcontroller with a 6-DoF MPU6886 accelerometer and gyroscope), it translates physical feline play vectors into microtonal acoustics and real-time 3D telemetry visualizations.

---

## Architecture & Data Flow

```
[ Physical Sphere Motion ]
           │
           ▼
[ MPU6886 6-DoF IMU ]
           │  (I2C Bus)
           ▼
[ ESP32-S3 Firmware: atom_s3_accel_udp.py ]
           │  (WiFi / UDP @ 30Hz)
           ▼
[ udp_ws_bridge.py / WebSocket Broker ]
      ├───► [ visualizer.html: 3D Cavalier, Projections, Heatmaps ]
      └───► [ Web Audio Microtonal Synth Engine ]
```

---

## File Structure

- `atom_s3_accel_udp.py`: MicroPython firmware for the M5Stack Atom S3. Samples IMU registers at ~30Hz and broadcasts binary UDP datagrams (`<ffff` struct: X, Y, Z, and total Magnitude).
- `udp_ws_bridge.py`: Lightweight Python asyncio bridge forwarding UDP packets to browser WebSockets.
- `visualizer.html`: Full real-time browser dashboard featuring 3D cavalier projections, orthogonal heatmaps (XY, XZ, YZ), auto-scaling acceleration waveforms, and audio synthesis.
- `secrets.py.example`: Configuration template for Wi-Fi SSID and target receiver IP.
- `osc_receiver_test.py`: Standalone UDP test listener for diagnostics.

---

## Quick Start

### 1. Configure Firmware
Copy `secrets.py.example` to `secrets.py` on your M5Stack Atom S3 and configure your local Wi-Fi:
```python
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"
TARGET_IP = "192.168.1.100"
TARGET_PORT = 5005
```
Upload `atom_s3_accel_udp.py` to the device via Thonny or `ampy`.

### 2. Start the WebSocket Bridge & Visualizer
```bash
# 1. Run the UDP-to-WebSocket bridge on the host machine
python3 udp_ws_bridge.py

# 2. Open visualizer.html in any modern web browser
```

---

## Author & License

Created by **Carlos Romero Madrid** ([@carrommad](https://github.com/carrommad))  
Computational Physicist & Creative Technologist · Barcelona Supercomputing Center (BSC-CNS)

Licensed under the [MIT License](LICENSE).
