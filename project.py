from utime import sleep
from machine import Pin

led = Pin("LED", Pin.OUT)

a1_rot = Pin(6, Pin.OUT)
a1_gelb = Pin(7, Pin.OUT)
a1_gruen = Pin(8, Pin.OUT)

a2_rot = Pin(18, Pin.OUT)
a2_gelb = Pin(19, Pin.OUT)
a2_gruen = Pin(20, Pin.OUT)


while True:
    try:
        led.toggle()
        a1_rot.toggle()
        a1_gelb.toggle()
        a1_gruen.toggle()
        a2_rot.toggle()
        a2_gelb.toggle()
        a2_gruen.toggle()
        sleep(2)
        led.off()
        a1_rot.off()
        a1_gelb.off()
        a1_gruen.off()
        a2_rot.off()
        a2_gelb.off()
        a2_gruen.off()
        sleep(2)
    except KeyboardInterrupt:
        break