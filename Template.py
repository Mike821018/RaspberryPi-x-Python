#!/usr/bin/env python3

from RPi import GPIO
from time import sleep


class LED: # pin 13, 15
    def __init__(self,pin):
        self.pin = pin
        GPIO.setup(self.pin,GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.pin,1)

    def off(self):
        GPIO.output(self.pin,0)

# High volt controlling way
class BUZZER: # pin 32
    def __init__(self,pin):
        self.pin = pin
        self.off()
    def on(self):
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,1)
    def off(self):
        GPIO.setup(self.pin,GPIO.IN)

class LCM:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.LCD_RS = 38
        self.LCD_RW = 40
        self.LCD_E  = 29
        self.LCD_D4 = 31
        self.LCD_D5 = 33
        self.LCD_D6 = 35
        self.LCD_D7 = 37

        self.CMD_DELAY = 0.005
        self.CMD_CLEAR_DELAY = 0.005
        self.reset()
    ## LCM setup
    def reset(self):
        # setup the pin out
        GPIO.setup(self.LCD_E,  GPIO.OUT) # E
        GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
        GPIO.setup(self.LCD_RW, GPIO.OUT) # RW
        GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

        # initialize the level of all pin
        GPIO.output(self.LCD_D4,0)
        GPIO.output(self.LCD_D5,0)
        GPIO.output(self.LCD_D6,0)
        GPIO.output(self.LCD_D7,0)
        GPIO.output(self.LCD_RS,0)
        GPIO.output(self.LCD_RW,0)
        GPIO.output(self.LCD_E,0)
        
        sleep(0.1)
        GPIO.output(self.LCD_E,1)
        sleep(0.000001)
        GPIO.output(self.LCD_E,0)
        sleep(0.000001)

        ### reset the LCD and use the 4 bit (4-lines) mode
        sleep(0.002)
        self.write_cmd(0x03)
        sleep(0.001)
        self.write_cmd(0x03)
        sleep(0.0001)
        self.write_cmd(0x03)
        sleep(0.0001)
        self.write_cmd(0x02)
        sleep(0.0001)
        ### end reset procedure
        
        # function setup 
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x01)
        sleep(self.CMD_CLEAR_DELAY)
        self.write_cmd(0x06)


    # sent command to LCM
    def write_cmd(self , cmd ):
        GPIO.output(self.LCD_RS, 0)
        GPIO.output(self.LCD_RW, 0)
        GPIO.output(self.LCD_E , 0)

        # write high 4 bits
        GPIO.output(self.LCD_D7, 1 if 0b10000000 & cmd else 0)
        GPIO.output(self.LCD_D6, 1 if 0b01000000 & cmd else 0)
        GPIO.output(self.LCD_D5, 1 if 0b00100000 & cmd else 0)
        GPIO.output(self.LCD_D4, 1 if 0b00010000 & cmd else 0)

        sleep(0.000001)
        GPIO.output(self.LCD_E, 1)
        sleep(0.000001)
        GPIO.output(self.LCD_E, 0)

        # write low 4 bits
        GPIO.output(self.LCD_D7, 1 if 0b00001000 & cmd else 0)
        GPIO.output(self.LCD_D6, 1 if 0b00000100 & cmd else 0)
        GPIO.output(self.LCD_D5, 1 if 0b00000010 & cmd else 0)
        GPIO.output(self.LCD_D4, 1 if 0b00000001 & cmd else 0)

        sleep(0.000001)
        GPIO.output(self.LCD_E, 1)
        sleep(0.000001)
        GPIO.output(self.LCD_E, 0)
        sleep( self.CMD_DELAY )
        

    # sent data to LCM
    def write_data(self , data):
        GPIO.output(self.LCD_RS, 1)
        GPIO.output(self.LCD_RW, 0)
        GPIO.output(self.LCD_E , 0)

        # write high 4 bits
        GPIO.output(self.LCD_D7, 1 if 0b10000000 & data else 0)
        GPIO.output(self.LCD_D6, 1 if 0b01000000 & data else 0)
        GPIO.output(self.LCD_D5, 1 if 0b00100000 & data else 0)
        GPIO.output(self.LCD_D4, 1 if 0b00010000 & data else 0)

        sleep(0.000001)
        GPIO.output(self.LCD_E, 1)
        sleep(0.000001)
        GPIO.output(self.LCD_E, 0)

        # write low 4 bits
        GPIO.output(self.LCD_D7, 1 if 0b00001000 & data else 0)
        GPIO.output(self.LCD_D6, 1 if 0b00000100 & data else 0)
        GPIO.output(self.LCD_D5, 1 if 0b00000010 & data else 0)
        GPIO.output(self.LCD_D4, 1 if 0b00000001 & data else 0)

        sleep(0.000001)
        GPIO.output(self.LCD_E, 1)
        sleep(0.000001)
        GPIO.output(self.LCD_E, 0)
        sleep( self.CMD_DELAY )


    ## Move the cursor to the destination
    ## line 1 ~ 1
    ## col  1 ~ 16
    def move(self,line=1,col=1):
        """
        move(line=1,col=1)
        line: 1 ~ 2
        col : 1 ~ 16
        """
        _pos = 0x80 + (line-1) * 0x40 + (col-1)
        self.write_cmd(_pos)


    ## Write data to where the cursor is (The cursor will automatically move to next char)
    def write_msg(self,msg):
        if type(msg) == str:
            data = [ord(i) for i in msg]
            for i in data:
                self.write_data(i)
    

    def clear_line_1(self):
        self.move(1,1)
        self.write_msg(' ' * 16)


    def clear_line_2(self):
        self.move(2,1)
        self.write_msg(' ' * 16)

### Important! Cause Raspberry pi has 2 different ways of declaring the GPIO pin###
GPIO.setmode(GPIO.BOARD) 
###
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
#########################
GPIO.add_event_detect(16, GPIO.BOTH, bouncetime=50)
GPIO.add_event_callback(16, yielling)
#########################
GPIO.cleanup()
