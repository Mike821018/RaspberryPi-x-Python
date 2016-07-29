#!/usr/bin/env python

import commands
from threading import Thread
from time import sleep

def scanning():
    commands.getoutput('sudo hcitool lescan')
    
def watching():
    return commands.getoutput('sudo hcidump')
    
def stop():
    commands.getoutput('')
    

# Not finished yet
