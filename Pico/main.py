import select
import sys
import time
from machine import I2C
from SH1106 import SH1106_I2C
import faceexpression as fe
import utime


# Define UART configuration
uart_id = 0
baud_rate = 9600
tx_pin = 0
rx_pin = 1

# Initialize UART
uart = machine.UART(uart_id, baudrate=baud_rate, tx=tx_pin, rx=rx_pin)

obj=fe.FacialExp()
# Loop indefinitely
i2c=I2C(1)
obj.initialize(i2c)
d=1
def is_float(text):
    try:
        float(text)
        return True
    except:
        return False

while True:
    # Wait for input on stdin
    obj.default_face()
    data=""
    while True:
    # Check if there is data available to read
        if uart.any():
        # Read and print the received data
            data = uart.read().decode("utf-8")
            print("Received:", data)
    
        utime.sleep(0.1)
    
        if(data=="greeting"):
            break
        elif(data=="introduction"):
            break
        elif(data=="farewell"):
            break
        elif(data=="polite"):
            break
        elif(data=="acknowledgement"):
            break
        elif(data=="apology"):
            break
        elif(data=="compliment"):
            break
        elif(data=="smart"):
            break
        elif(data=="affirmation"):
            break
        elif(is_float(data)):
            d=float(data)
            data=""
            break
    print(d,"\n")    
    if(data=="greeting"):
        obj.happy_face()
        time.sleep(d)
    elif(data=="intoduction"):
        obj.default_face()
        time.sleep(d)
    elif(data=="farewell"):
        obj.sad_face()
        time.sleep(d)
        obj.sleep_face(5)
    elif(data=="polite"):
        obj.happy_face()
        time.sleep(d)
    elif(data=="acknowledgement"):
        obj.love_face()
        time.sleep(d)
    elif(data=="compliment"):
        obj.happy_face()
        time.sleep(d)
    elif(data=="apology"):
        obj.sad_face()
        time.sleep(d)
    elif(data=="smart"):
        obj.wink_face()
        time.sleep(d)
    elif(data=="affirmation"):
        obj.eyeclose_face()
        time.sleep(d)
        