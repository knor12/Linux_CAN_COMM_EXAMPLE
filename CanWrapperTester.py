

#!/usr/bin/python3

from __future__ import print_function

import can
import time
from CanWrapper import *

can_interface = 'can0'

def handleRxFrame_1(message):
    print("handler 1 received message"+str(message) + "\n")
    
def handleRxFrame_2(message):
    print("handler 2 received message"+str(message)+ "\n")
    
def handleTxFrame(message):
    print("Sent message"+str(message)+ "\n")    

def main():
    canwrapper = CanWrapper(can_interface_name='can0')
    canwrapper.open()
    canwrapper.setReceiveHandler(handleRxFrame_1)
    #bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    msg = can.Message(arbitration_id=0xff,data=[0, 0x25, 0x0, 0x1, 0x3, 0x1, 0x4, 0x1],extended_id=False)
    i = 5
    while(i>0) :
        try:
            i=i-1
            canwrapper.sendMessage(msg)
            time.sleep(1)
        except BaseException as e:
            logging.error("Error sending can message {%s}: %s" % (msg, e))

    canwrapper.close()
    canwrapper.open()
    canwrapper.setReceiveHandler(handleRxFrame_2)
    canwrapper.setSentHandler(handleTxFrame)
    i=5
    while(i>0) :
        try:
            i=i-1
            canwrapper.sendMessage(msg)
            time.sleep(1)
        except BaseException as e:
            logging.error("Error sending can message {%s}: %s" % (msg, e))
    
    canwrapper.close()
if __name__ == "__main__":
    main()