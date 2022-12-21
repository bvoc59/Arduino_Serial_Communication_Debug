# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 12:36:48 2022
@author: BVoci
"""

import serial, time, sys

BAUD_RATE      = 128000
COM_PORT       = 'COM9'

MESSAGE_SIZE   = 4
MESSAGE_FORMAT = 'utf-8' 

arduino      = None 
arduino_open = False 
arduino_out  = None 
message      = [' ']*MESSAGE_SIZE 

t1 = 0 
t2 = 0 
t3 = 0 

print("ARDUINO SERIAL COMMUNICATION DEBUG INTERFACE (ASCDI)")

print("PORT INFORMATION: ") 
print("Baud Rate: " + str(BAUD_RATE))
print("COM  Port: " + COM_PORT)

print("MESSAGE INFORMATION: ")
print("Message Size:   " + str(MESSAGE_SIZE) + " bytes") 
print("Message Format: " + MESSAGE_FORMAT)

def init_arduino(): 
    
    global arduino 
    
    try:
        arduino = serial.Serial(
            port     = COM_PORT,
            baudrate = BAUD_RATE, 
            bytesize = serial.EIGHTBITS, 
            timeout  = 2, 
            stopbits = serial.STOPBITS_ONE) 
        return 1 
    except serial.SerialException: 
        return 0 
    
def display_arduino_out(): 
    
    global t1,t2,t3 
    global arduino_out 
    
    print("Arduino Response: " + str(arduino_out)) 
    print(f"Write Time [ms]: {1000*(t2 - t1):0.8f}\n")
    print(f"Read  Time [ms]: {1000*(t3 - t2):0.8f}\n")
    print(f"Total      [ms]: {1000*(t3 - t1):0.8f}\n")


if init_arduino(): 
    arduino_open = True     
    while arduino_open: 
        for i in range(MESSAGE_SIZE):
            message[i] = input("Enter message[" + str(i) + "]: ")
        
        if(message[0] == "EXIT"):
            if arduino_open:
                print("Closing Arduino...")
                arduino.close()
            print("Exiting ASCDI...") 
            sys.exit()
        else: 
            
            print("Writing message...") 
            try:  
                
               t1 = time.perf_counter() 
               for i in range(MESSAGE_SIZE):
                    arduino.write(bytes(message[i], MESSAGE_FORMAT)) 
               t2 = time.perf_counter() 
               
               arduino_out = arduino.readline() 
               t3          = time.perf_counter() 
               
               print("Reading response...")
               display_arduino_out() 
                
            except serial.SerialException: 
                arduino_open = False
    
    print("Arduino unexpectedly closed!")
    print("Exiting ASCDI...")
    sys.exit() 

else: 
    print("Unable to connect to Arduino!")
    print("Exiting ASCDI...") 
    sys.exit()
    
