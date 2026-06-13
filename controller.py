from utime import ticks_ms, ticks_diff
import traffic_lights
from config import GREEN_DURATION_MS, TRANSITION_DURATION_MS, ALL_RED_DURATION_MS, MIN_GREEN_MS

# (cars_r, cars_y, cars_g, peds_r, peds_y, peds_g, duration_ms)
STATES = [
    (0, 0, 1, 1, 0, 0, GREEN_DURATION_MS),
    (0, 1, 0, 1, 0, 0, TRANSITION_DURATION_MS),
    (1, 0, 0, 1, 0, 0, ALL_RED_DURATION_MS),
    (1, 0, 0, 1, 1, 0, TRANSITION_DURATION_MS),
    (1, 0, 0, 0, 0, 1, GREEN_DURATION_MS),
    (1, 0, 0, 0, 1, 0, TRANSITION_DURATION_MS),
    (1, 0, 0, 1, 0, 0, ALL_RED_DURATION_MS),
    (1, 1, 0, 1, 0, 0, TRANSITION_DURATION_MS),
]

STATE_CARS_GREEN = 0
STATE_PEDS_GREEN = 4

state = {
    "current": STATE_CARS_GREEN,
    "start": ticks_ms(),
    "cars_request": False,
    "pedestrian_request": False,
}


def switch_to(index):
    state["current"] = index
    state["start"] = ticks_ms()
    s = STATES[index]
    traffic_lights.set_lights(s[0], s[1], s[2], s[3], s[4], s[5])


def update():
    elapsed_time = ticks_diff(ticks_ms(), state["start"])

    if elapsed_time >= STATES[state["current"]][6]:
        switch_to((state["current"] + 1) % len(STATES))
        return

    if state["pedestrian_request"] and state["current"] == STATE_CARS_GREEN and elapsed_time >= MIN_GREEN_MS:
        state["pedestrian_request"] = False
        switch_to(STATE_CARS_GREEN + 1)
        return

    if state["cars_request"] and state["current"] == STATE_PEDS_GREEN and elapsed_time >= MIN_GREEN_MS:
        state["cars_request"] = False
        switch_to(STATE_PEDS_GREEN + 1)

