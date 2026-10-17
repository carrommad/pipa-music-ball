import network, socket, struct, gc, time
from machine import Pin, I2C

try:
    from secrets import WIFI_SSID, WIFI_PASS, TARGET_IP, TARGET_PORT
except ImportError:
    WIFI_SSID   = "YOUR_WIFI_SSID"
    WIFI_PASS   = "YOUR_WIFI_PASSWORD"
    TARGET_IP   = "192.168.1.100"
    TARGET_PORT = 5005

# WiFi - connect if not connected
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(2)
if not wlan.isconnected():
    wlan.connect(WIFI_SSID, WIFI_PASS)
    for _ in range(20):
        if wlan.isconnected(): break
        time.sleep(1)
print("IP:", wlan.ifconfig()[0])

# MPU6886 IMU initialization (I2C)
i2c = I2C(0, sda=Pin(38), scl=Pin(39), freq=400000)
i2c.writeto_mem(0x68, 0x6B, bytes([0x00]))
i2c.writeto_mem(0x68, 0x1C, bytes([0x10]))
SCALE = 8.0 / 32768.0

gc.collect()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (TARGET_IP, TARGET_PORT)
print("Streaming inertial telemetry @ 30Hz to", addr)

while True:
    d = i2c.readfrom_mem(0x68, 0x3B, 6)
    x = struct.unpack('>h', d[0:2])[0] * SCALE
    y = struct.unpack('>h', d[2:4])[0] * SCALE
    z = struct.unpack('>h', d[4:6])[0] * SCALE
    mag = (x*x+y*y+z*z)**0.5
    sock.sendto(struct.pack('<ffff', x, y, z, mag), addr)
    time.sleep_ms(33)
