# dummy lib
"""
dummy library to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

# consts
DEEPSLEEP_RESET  =0
 
import re as ure

# classes 
class PWM:
  def __init__(self,a):
    return
  def freq(self,a=0):
    return 0
  def duty(self,a=0):
    return 0


class Pin:
  IN=1
  OUT=2
  def __init__(self,a=0,b=0):
    return
  def value(self,a=0):
    return 0
    
    
class ADC:
  def __init__(self,a):
    return
  def read_u16(self):
    return 0
  def read(self):
    return 0
    

class Timer:
  def __init__(self,id=0):
    return
  def init(self,period=0, callback=0, mode=0):
    return
  def deinit(self):
    return
    
class RTC:
  def __init__(self,id=0):
    return
  def datetime(self,i=0):
    return "0"
    
class UART:
  def __init__(self,id=0):
    return

class WDT:
  def __init__(self):
    return
        
# funcs    
def reset():
  return
def deepsleep():
  return
def enable_irq(): return 0
def disable_irq(): return 0
def unique_id(): return 0
def reset_cause(): return 0

#eof
