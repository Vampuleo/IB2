# at zero, cycle is 10 ms
# as we want it to become more bright, sleep time decrease while on time increase

from gpiozero import LED, Button
from time import sleep
from signal import pause

count = 0
c_next = 0
sleep_val = 10
on_val = 0

led = LED(2)
button = Button(3)


def counter():
    global count, c_next, sleep_val, on_val

    if c_next <= 10:
        count = c_next
        c_next += 1
        sleep_val = sleep_val - 1
        on_val = on_val + 1
        print("count is: " + str(count))


def brightness():
    counter()
    led.on()
    sleep(on_val * 0.01)
    led.off()
    sleep(sleep_val * 0.01)


while True:
    button.when_activated = brightness
    if c_next == 10:
        c_next = 0
        sleep_val = 10
        on_val = 0


