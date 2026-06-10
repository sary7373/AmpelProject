from utime import sleep
from machine import Pin

led = Pin("LED", Pin.OUT)

traffic_lights = {
    "cars": {
        "red": Pin(6, Pin.OUT), 
        "yellow": Pin(7, Pin.OUT), 
        "green": Pin(8, Pin.OUT)
        },
    "pedestrians": {
        "red": Pin(18, Pin.OUT), 
        "yellow": Pin(19, Pin.OUT), 
        "green": Pin(20, Pin.OUT)
        }
}


def red_to_green(traffic_light):
        traffic_lights[traffic_light]["yellow"].on()
        sleep(2)
        traffic_lights[traffic_light]["red"].off()
        traffic_lights[traffic_light]["yellow"].off()
        traffic_lights[traffic_light]["green"].on()

def green_to_red(traffic_light):
        traffic_lights[traffic_light]["green"].off()
        traffic_lights[traffic_light]["yellow"].on()
        sleep(2)
        traffic_lights[traffic_light]["red"].on()
        traffic_lights[traffic_light]["yellow"].off()

def all_lights_off():
    for traffic_light in traffic_lights.values():
        for light in traffic_light.values():
            light.off()

def get_light_color(traffic_light):
    if traffic_lights[traffic_light]["green"].value() == 1:
        return "green"
    if traffic_lights[traffic_light]["red"].value() == 1:
        return "red"
    return "other"

def switch_lights(light_a, light_b):
    color_a = get_light_color(light_a)
    color_b = get_light_color(light_b)

    if color_a == "green" and color_b == "red":
        currently_green = light_a
        currently_red = light_b
    elif color_b == "green" and color_a == "red":
        currently_green = light_b
        currently_red = light_a
    else:
        raise ValueError("switch_lights expects one green and one red traffic light")

    green_to_red(currently_green)
    sleep(1)
    red_to_green(currently_red)


all_lights_off()
traffic_lights["cars"]["red"].on()
traffic_lights["pedestrians"]["green"].on()
while True:
    try:
        sleep(5)
        switch_lights("cars", "pedestrians")
        sleep(5)
        switch_lights("cars", "pedestrians")
    except KeyboardInterrupt:
        break