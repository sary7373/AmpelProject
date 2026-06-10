from utime import sleep
from machine import Pin

led = Pin("LED", Pin.OUT)

a1_red = Pin(6, Pin.OUT)
a1_yellow = Pin(7, Pin.OUT)
a1_green = Pin(8, Pin.OUT)

a2_red = Pin(18, Pin.OUT)
a2_yellow = Pin(19, Pin.OUT)
a2_green = Pin(20, Pin.OUT)


def red_to_green(traffic_light):
    if traffic_light == 1:
        a1_yellow.toggle()
        sleep(2)
        a1_red.off()
        a1_yellow.off()
        a1_green.on()
    elif traffic_light == 2:
        a2_yellow.toggle()
        sleep(2)
        a2_red.off()
        a2_yellow.off()
        a2_green.on()


def green_to_red(traffic_light):
    if traffic_light == 1:
        a1_green.off()
        a1_yellow.on()
        sleep(2)
        a1_red.on()
        a1_yellow.off()
    elif traffic_light == 2:
        a2_green.off()
        a2_yellow.on()
        sleep(2)
        a2_red.on()
        a2_yellow.off()

a1_red.on()
a2_green.on()
while True:
    try:
        sleep(5)
        green_to_red(2)
        red_to_green(1)
        sleep(5)
        green_to_red(1)
        red_to_green(2)
        sleep(5)
    except KeyboardInterrupt:
        break