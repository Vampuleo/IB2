from gpiozero import LED, Button
from signal import pause

led = LED(26)
button = Button(2)

button.when_pressed = led.on
button.when_released = led.off

pause()
