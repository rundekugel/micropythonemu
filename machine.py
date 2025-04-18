# dummy lib
"""
dummy library to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

import serial
import socket

# consts
__version__ = "0.1.0.2"
DEEPSLEEP_RESET = 0

import os
import uuid
import time
import threading

ismicropython = False
try:
  if "ESP" in os.uname().machine:
    ismicropython = True
    print("warning! don't use this on micropython. "
          "It's intended to be used on python3 !")
except:
  pass
  
import re as ure

# classes
class emuSettings:
  useGui = True
try:
  import halEmu
except:
  halEmu = None
  emuSettings.useGui=False

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
  maxPins =39
  guiupdateinterval=0.2
  _guiupdatethread = None
  
  def __init__(self, num=0, mode=-1, value=0, *args, **k):
    self.num = num
    if emuSettings.useGui:
      if not halEmu.obj:
        halEmu.obj = halEmu.Gui(maxPins=self.maxPins)
        # this doesn't work anymore, cause TK want's the main thread sind py3.9
        # self._guiupdatethread = threading.Thread(target=self.doGuiupdateThread)
        # self._guiupdatethread.start()
        # halEmu.obj.gui.update() # once isn't enough. we must call it repeatedly
      self.mode(mode)
      if value: halEmu.obj.setPin(num,value)
    return

  def doGuiupdateThread(self, interval=0.2):
    while self._guiupdatethread:
      halEmu.obj.gui.update()
      time.sleep(self.guiupdateinterval)

  def doGuiupdate(self):
      halEmu.obj.gui.update()

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
  ATTN_11DB = None
  def __init__(self,*a):
    if emuSettings.useGui:
      if not halEmu.obj:
        halEmu.obj = halEmu.Gui(maxPins=10)

  def read_u16(self):
    return halEmu.obj.getAdc()
  def read(self):
    return halEmu.obj.getAdc()
  def atten(self, *args, **kargs):
    return
  def read_uv(self):
    return halEmu.obj.getAdc()

class Timer:
  def __init__(self,id=0):
    return
  def init(self,period=0, callback=0, mode=0):
    return
  def deinit(self):
    return
    
class RTC:
  memoryData = b""
  def __init__(self,id=0):
    return
  def datetime(self,i=0):
    return (1,1,1,1,1,1,1)
  def memory(self, data=None):
    if data:
      self.memoryData = data
    return self.memoryData
    
class UART:
  """redirect upython uart to dev/tty..."""
  # todo: redirect to tcp/ip port for better debugging
  _s = None
  port = "/dev/ttyUSB0"  # linux
  port = "/dev/pts/2"    # linux terminal
  tcp = ("localhost",8888) # tcp/ip
  client = None
  # port = "com31"  # windows
  baudrate = 115200
  timeout_ms = 0
  stopbits=1

  def __init__(self, port=None, baudrate=None, *args, **kwargs):
    # def __init__(self, port=None, baudrate=None):
    if baudrate: self.baudrate = baudrate
    r= kwargs.get("timeout")
    if r: self.timeout_ms = r
    k={"port":self.port, "baudrate":self.baudrate,
       "timeout":int(self.timeout_ms/1000), "stopbits":self.stopbits}
    if self.tcp:
      try:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.tcp)
        self.client.settimeout(.2)
      except:
        pass
    else:
      self._s=serial.Serial(**k)
  def read(self, cnt=None):
    if self.client:
      r=b""
      try:
        r=self.client.recv(100)  #.decode()
      finally:
        return r
    else:
      return self._s.read()
  def write(self, data):
    if not isinstance(data, bytes):
      data = data.encode()
    if self.client:
      try:
        return self.client.send(data)
      except:
        return 0
    else:
      try:
        return self._s.write(data)
      except:
        return 0
  def readline(self, cnt=None):
    return self._s.readline(cnt)
  def close(self):
    if tcp:
      self.client.close()
      self.client=None
    else:
      self._s.close()
  def any(self):
    return "sa"

class WDT:
  def __init__(self,  *args, **kargs):
    return
  def feed(self,  *args, **kargs):
    return
    
class SoftI2C:
   """dummy implementation"""    
   def __init__(self, *args, **kargs):
       return
   def readfrom_mem(self, adr=0, len=1, *args, **kargs):
     return bytes(len)
   def readfrom(self, adr=0, len=1, *args, **kargs):
     return bytes(len)
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
def deepsleep(ms=0, *args, **kargs):
  time.sleep(ms/1000)
  return
def enable_irq(): return 0
def disable_irq(): return 0
def unique_id(): return uuid.uuid4().bytes
def reset_cause(): return 0

#eof
