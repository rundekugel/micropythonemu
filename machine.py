# dummy lib
"""
dummy library to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

# consts
DEEPSLEEP_RESET  =0
 
import re as ure
try:
  import halEmu
except:
  halEmu = None
  emuSettings.useGui=False

# classes
class emuSettings:
  useGui = True

class PWM:
  def __init__(self,a):
    return
  def freq(self,a=0):
    return 0
  def duty(self,a=0):
    return 0


class Pin:
  IN=0
  OUT=1
  OPEN_DRAIN=2
  PULL_UP =1
  PULL_DOWN=None
  IRQ_FALLING=2
  IRQ_RISING=1
  IRQ_LOW_LEVEL=None
  IRQ_HIGH_LEVEL=None
  num=None
  mode=None

  def __init__(self, num=0, mode=-1, value=0, *args, **k):
    self.num = num
    if emuSettings.useGui:
      if not halEmu.obj:
        halEmu.obj = halEmu.Gui(maxPins=10)
      self.mode(mode)
      if value: halEmu.obj.setPin(value)
    return

  def value(self, val=None):
    if not emuSettings.useGui: return 0
    if val is not None:
      halEmu.obj.setPin(self.num, val)
    return halEmu.obj.getPinState(self.num)

  def irq(self, handler=None, trigger=2 | 1,
          priority=1, wake=None, hard=False):
    halEmu.setIrq(handler, self.num, trigger)

  def mode(self, mode=-1):
    """not for esp8266"""
    if not emuSettings.useGui: return
    if mode == self.OUT:
      halEmu.obj.setPinDir(num, 1)

  def on(self):
    self.value(1)
  def off(self):
    self.value(0)


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
