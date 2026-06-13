from machine import Pin

cars_red = Pin(6, Pin.OUT)
cars_yellow = Pin(7, Pin.OUT)
cars_green = Pin(8, Pin.OUT)

peds_red = Pin(18, Pin.OUT)
peds_yellow = Pin(19, Pin.OUT)
peds_green = Pin(20, Pin.OUT)


def set_lights(c_r, c_y, c_g, p_r, p_y, p_g):
    cars_red.value(c_r)
    cars_yellow.value(c_y)
    cars_green.value(c_g)
    peds_red.value(p_r)
    peds_yellow.value(p_y)
    peds_green.value(p_g)


def all_lights_off():
    set_lights(0, 0, 0, 0, 0, 0)

