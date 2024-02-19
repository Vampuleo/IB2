from gpiozero import LED, Button

led1 = LED(26)
led2 = LED(19)
led3 = LED(13)
led4 = LED(6)
button1 = Button(3)
button2 = Button(2)
count = 0
c_next = 0
holder = 0
buffer_value = 0
button1_active = True


# method to display
def display(array):
    if array[0] == 1:
        led1.on()
    else:
        led1.off()
    if array[1] == 1:
        led2.on()
    else:
        led2.off()
    if array[2] == 1:
        led3.on()
    else:
        led3.off()
    if array[3] == 1:
        led4.on()
    else:
        led4.off()


def counter():
    global count, c_next

    if button1_active and count < 16:
        binary_holder = format(c_next, '04b')
        bit_list = [int(bit) for bit in binary_holder]
        print(bit_list)
        print("count is: " + str(c_next))
        display(bit_list)
        count = c_next
        c_next += 1


def buffer():
    global holder
    global buffer_value
    if count < 0 or count <= 0:
        print("buffer value not possible yet")
    else:
        for i in range(5):
            holder += 1
            if count < 0:
                for j in range(holder):
                    buffer_value += count
            else:
                buffer_value += count

        if (holder - 1) < 1:
            div_val = 1
        else:
            div_val = holder
        # makes value a whole number
        buffer_value = int(buffer_value / (div_val - 1))
        binary_buffer_value = format(buffer_value, '04b')
        bit_list = [int(bit) for bit in binary_buffer_value]
        print("buffer value: " + str(bit_list))
        print("count is: " + str(c_next))
        display(bit_list)


while c_next <= 16:

    button1.when_activated = counter
    button2.when_activated = buffer

    if c_next == 16:
        c_next = 0

# have to use c_next because it prepares next "cycle"
# count holds data of previous cycle, needed for buffer calc
