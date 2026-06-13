import network
import traffic_lights
import controller
import web_server
from config import SSID, PASSWORD


def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)
    while not ap.active():
        pass


start_access_point()
traffic_lights.all_lights_off()
controller.switch_to(0)
web_server.start()

while True:
    web_server.handle_request()
    controller.update()

