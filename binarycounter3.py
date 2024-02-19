from gpiozero import LED, Button
from time import sleep
from signal import pause

led_status = False
led1 = LED(26)
led2 = LED(19)
led3 = LED(13)
led4 = LED(6)
button1 = Button(3)
button2 = Button(2)
count = 0

list1 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
list2 = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
list3 = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
list4 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]


def binary_counter():
    global count
    if count < 16:
        if list1[count] == 0:
            led1.off()
        else:
            led1.on()

        if list2[count] == 0:
            led2.off()
        else:
            led2.on()

        if list3[count] == 0:
            led3.off()
        else:
            led3.on()

        if list4[count] == 0:
            led4.off()
        else:
            led4.on()

        count += 1


while count <= 16:
    button1.when_activated = binary_counter
    if count == 15:
        count = 0

