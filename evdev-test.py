from evdev import UInput, ecodes as e
import time

ui = UInput()
for x in range(10):
    time.sleep(1)
    ui.write(e.EV_KEY, e.KEY_A, 1)
    ui.write(e.EV_KEY, e.KEY_A, 0)
    ui.syn()

ui.close()