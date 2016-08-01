#!/usr/bin/env python

import commands
from threading import Thread
from time import sleep

def scanning():
    commands.getoutput('sudo hcitool lescan')
    
def watching():
    return commands.getoutput('sudo hcidump')
    
def stop():
    return commands.getoutput('\x03')
    
threating.Thread(target = scanning)
sleep(3)
tmp = commands.getoutput('\x03')
    

# Not finished yet
