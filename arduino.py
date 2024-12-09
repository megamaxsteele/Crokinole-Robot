import pyfirmata2
import time

PORT =  pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)

print("Success")

while(True):
    board.digital[13].write(1)
    time.sleep(1)
    board.digital[13].write(0)
    time.sleep(1)