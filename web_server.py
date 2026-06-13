import socket
import controller

HTML = b"""\
HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n\
<!DOCTYPE html>
<html>
  <head><title>Ampelschaltung</title></head>
  <body>
    <h1>Traffic Lights</h1>
    <button onclick="req('/cars')">cars: request green</button>
    <button onclick="req('/pedestrians')">pedestrians: request green</button>
    <script>
    function req(path) { 
        fetch(path).catch(() => {}); 
    }
    </script>
  </body>
</html>"""

NOT_FOUND = b"HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n"

server = {"socket": None}


def start():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 80))
    sock.listen(1)
    sock.setblocking(False)
    server["socket"] = sock


def handle_request():
    try:
        conn, _ = server["socket"].accept()
    except OSError:
        return

    try:
        conn.settimeout(0.1)
        request = b''
        try:
            request = conn.recv(1024)
        except OSError:
            pass

        if b'/favicon.ico' in request:
            conn.send(NOT_FOUND)
        elif b'/cars' in request:
            controller.state["cars_request"] = True
            conn.sendall(HTML)
        elif b'/pedestrians' in request:
            controller.state["pedestrian_request"] = True
            conn.sendall(HTML)
        else:
            conn.sendall(HTML)
    finally:
        conn.close()

