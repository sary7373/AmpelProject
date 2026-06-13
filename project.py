from utime import ticks_ms, ticks_diff
from machine import Pin
import socket
import network


led = Pin("LED", Pin.OUT)

traffic_lights = {
    "cars": {
        "red":    Pin(6,  Pin.OUT),
        "yellow": Pin(7,  Pin.OUT),
        "green":  Pin(8,  Pin.OUT),
    },
    "pedestrians": {
        "red":    Pin(18, Pin.OUT),
        "yellow": Pin(19, Pin.OUT),
        "green":  Pin(20, Pin.OUT),
    }
}


ap = network.WLAN(network.AP_IF)
ap.config(essid='AmpelPico', password='12345678')
ap.active(True)
while not ap.active():
    pass


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 80))
server.listen(1)
server.setblocking(False)


def all_lights_off():
    for traffic_light in traffic_lights.values():
        for light in traffic_light.values():
            light.off()

# Zustände: (cars_r, cars_y, cars_g, peds_r, peds_y, peds_g, dauer_ms)
STATES = [
    (0, 0, 1,  1, 0, 0,  8000),   # Autos grün
    (0, 1, 0,  1, 0, 0,  2000),   # Autos gelb
    (1, 0, 0,  1, 0, 0,   500),   # Alle rot
    (1, 0, 0,  1, 1, 0,  2000),   # Fussgänger rot+gelb
    (1, 0, 0,  0, 0, 1,  8000),   # Fussgänger grün
    (1, 0, 0,  0, 1, 0,  2000),   # Fussgänger gelb
    (1, 0, 0,  1, 0, 0,   500),   # Alle rot
    (1, 1, 0,  1, 0, 0,  2000),   # Autos rot+gelb
]

def apply_state(state_index):
    s = STATES[state_index]
    traffic_lights["cars"]["red"].value(s[0])
    traffic_lights["cars"]["yellow"].value(s[1])
    traffic_lights["cars"]["green"].value(s[2])
    traffic_lights["pedestrians"]["red"].value(s[3])
    traffic_lights["pedestrians"]["yellow"].value(s[4])
    traffic_lights["pedestrians"]["green"].value(s[5])


all_lights_off()
current_state = 0
apply_state(current_state)
state_start = ticks_ms()

html = """<!DOCTYPE html>
<html>
  <head><title>Ampelschaltung</title></head>
  <body>
    <h1>Traffic lights</h1>
    <p>Hello cars and pedestrians</p>
  </body>
</html>
"""


while True:
    try:
        conn, addr = server.accept()
        conn.setblocking(False)
        try:
            conn.recv(1024)
        except OSError:
            pass
        conn.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
        conn.send(html)
        conn.close()
    except OSError:
        pass

    if ticks_diff(ticks_ms(), state_start) >= STATES[current_state][6]:
        current_state = (current_state + 1) % len(STATES)
        apply_state(current_state)
        state_start = ticks_ms()