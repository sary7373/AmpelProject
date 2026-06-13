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


DEFAULT_GREEN_TIME = 8000
DEFAULT_TRANSITION_TIME = 2000
DEFAULT_ALL_RED_TIME = 500

# Zustände: (cars_r, cars_y, cars_g, peds_r, peds_y, peds_g, dauer_ms)
STATES = [
    (0, 0, 1, 1, 0, 0, DEFAULT_GREEN_TIME),   # Autos grün
    (0, 1, 0, 1, 0, 0, DEFAULT_TRANSITION_TIME),   # Autos gelb
    (1, 0, 0, 1, 0, 0, DEFAULT_ALL_RED_TIME),   # Alle rot
    (1, 0, 0, 1, 1, 0, DEFAULT_TRANSITION_TIME),   # Fussgänger rot+gelb
    (1, 0, 0, 0, 0, 1, DEFAULT_GREEN_TIME),   # Fussgänger grün
    (1, 0, 0, 0, 1, 0, DEFAULT_TRANSITION_TIME),   # Fussgänger gelb
    (1, 0, 0, 1, 0, 0, DEFAULT_ALL_RED_TIME),   # Alle rot
    (1, 1, 0, 1, 0, 0, DEFAULT_TRANSITION_TIME),   # Autos rot+gelb
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
    <h1>Traffic Lights</h1>
      <button onclick="request('/cars')">cars: request green</button>
      <button onclick="request('/pedestrians')">pedestrians: request green</button>
      <script>
      function request(path) {
        fetch(path).catch(() => {});
      }
    </script>
  </body>
</html>
"""


cars_request = False
pedestrian_request = False

MIN_GREEN_MS = 3000

while True:
    try:
        conn, addr = server.accept()
        conn.settimeout(0.1)
        request = b''
        try:
            request = conn.recv(1024)
        except OSError:
            pass

        if b'/favicon.ico' in request:
            conn.send(b'HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n')
        elif b'/cars' in request:
            cars_request = True
            print("car requested")
            conn.send(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            conn.sendall(html.encode('utf-8'))
        elif b'/pedestrians' in request:
            pedestrian_request = True
            print("ped requested")
            conn.send(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            conn.sendall(html.encode('utf-8'))
        else:
            conn.send(b'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n')
            conn.sendall(html.encode('utf-8'))

        conn.close()
    except OSError:
        pass

    now = ticks_ms()
    elapsed = ticks_diff(now, state_start)

    if elapsed >= STATES[current_state][6]:
        current_state = (current_state + 1) % len(STATES)
        apply_state(current_state)
        state_start = now

    elif (pedestrian_request
          and current_state == 0
          and elapsed >= MIN_GREEN_MS):
        current_state = 1
        apply_state(current_state)
        state_start = now
        pedestrian_request = False


    elif (cars_request
          and current_state == 4
          and elapsed >= MIN_GREEN_MS):
        current_state = 5
        apply_state(current_state)
        state_start = now
        cars_request = False