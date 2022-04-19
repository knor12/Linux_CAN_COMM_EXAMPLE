import can
import time
import logging
import threading
import os 

class CanWrapper ():

    def __init__(self , can_interface_name='can0', can_bus_type='socketcan_native', BaudRate=100000):
    
        self.can_interface_name = can_interface_name
        self.can_bus_type = can_bus_type
        self.isRunning=True
        self.FrameSentdHandeler = None
        self.BaudRate = BaudRate
        
        
    def open(self ):
        #/*down*/
        command = "sudo ip link set "+ self.can_interface_name +" down"
        os.system(command)
        #/*configure*/
        command =  "sudo ip link set "+ self.can_interface_name +" up type can bitrate " + str(self.BaudRate)
        os.system(command)
        self.bus = can.interface.Bus(channel=self.can_interface_name, bustype=self.can_bus_type)
        self.isRunning=True
        
        
    def close(self ):
        #add all bus cleanup here
        self.isRunning=False
        self.FrameSentdHandeler=None
        FrameReceviedHandeler=None
        
        #wait for the tx handler thread to stop running
        #if not (self.rxThread is None) and (self.rxThread.is_alive()):
            #self.rxThread.join()
        
        
    def sendMessage(self ,message):
        if not self.isRunning:
            return 
        try:    
            self.bus.send(message)
            if not (self.FrameSentdHandeler is None):
                self.FrameSentdHandeler(message)
            return True
        except BaseException as e:
            logging.error("Error sending can message {%s}: %s" % (message, e))
            return False
            
    def setSentHandler(self , FrameSentdHandeler):
        self.FrameSentdHandeler =FrameSentdHandeler;
        
    def setReceiveHandler(self , FrameReceviedHandeler):
        self.FrameReceviedHandeler =FrameReceviedHandeler;
        
        #spawn a thread to handle received messages
        self.rxThread = threading.Thread(target=self.__rx_thread_function)
        self.rxThread.start()
        
        
    def __rx_thread_function(self):
        if self.bus is None:
            print ("bus not initialized")
            return
            
        #listen for incoming frames, it is ok to block while listening
        while self.isRunning:
            message = self.bus.recv(0.1)
            if (not (message is None)) and (not(self.FrameReceviedHandeler is None)):
                self.FrameReceviedHandeler(message)
            
            

        #if we reached this point we can simply exit the thread        
