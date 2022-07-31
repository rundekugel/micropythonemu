# dummy lib
"""
dummy library to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

import serial

# consts
__version__ = "0.1.0.2"
DEEPSLEEP_RESET = 0

import os
import uuid

ismicropython = False
try:
  if "ESP" in os.uname().machine:
    ismicropython = True
    print("warning! don't use this on micropython. "
          "It's intended to be used on python3 !")
except:
  pass
  
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
    halEmu.obj.setIrq(handler, self.num, trigger)

  def mode(self, mode=-1):
    """not for esp8266"""
    if not emuSettings.useGui: return
    if mode == self.OUT:
      halEmu.obj.setPinDir(self.num, 1)

  def on(self):
    self.value(1)
  def off(self):
    self.value(0)


class ADC:
  def __init__(self,*a):
    if emuSettings.useGui:
      if not halEmu.obj:
        halEmu.obj = halEmu.Gui(maxPins=10)

  def read_u16(self):
    return halEmu.obj.getAdc()
  def read(self):
    return halEmu.obj.getAdc()
    

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
  _s = None
  port = "/dev/ttyUSB0"  # linux
  # port = "com31"  # windows
  baudrate = 115200
  timeout_ms = 0
  stopbits=1

  def __init__(self, *args, port=None, baudrate=None, **kwargs):
    # def __init__(self, port=None, baudrate=None):
    if baudrate: self.baudrate = baudrate
    r= kwargs.get("timeout")
    if r: self.timeout_ms = r
    k={"port":self.port, "baudrate":self.baudrate,
       "timeout":int(self.timeout_ms/1000), "stopbits":self.stopbits}
    self._s=serial.Serial(**k)
  def read(self, cnt=None):
    return self._s.read()
  def write(self, data):
    if not isinstance(data, bytes):
      data = data.encode()
    return self._s.write(data)
  def readline(self, cnt=None):
    return self._s.readline(cnt)
  def close(self):
    self._s.close()

class WDT:
  def __init__(self):
    return
        
# funcs    
def _isMicropython():
  res = False
  try:
    if os.uname()[0] == "esp8266":
      ismicropython = True
      return 
  finally:
    return False
    
def reset():
  return
def deepsleep():
  return
def enable_irq(): return 0
def disable_irq(): return 0
def unique_id(): return uuid.uuid4().bytes
def reset_cause(): return 0

#eof
