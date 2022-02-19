# dummy lib
"""
library to emulate esp8266 hardware for micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

import machine
import tkinter as tk
import time


# consts
 

# classes 
class Pin:
  """pin emulator"""
  DIRECTION_IN = 0
  DIRECTION_OUT = 1
  state = 0
  direction = 0 
  guiCb = None
  pinNum = None
  
  def __init__(self, pinnum, guiCb=None):
    self.pinnum=pinnum
    if guiCb: self.guiCb = guiCb
    
  def set(self,hiLo):
    if self.state == hiLo: return
    self.state = hiLo
    if self._guiCb:
      self._guiCb(self)    
      
  def setDir(self,inOut):
    if self.direction == inOut: return
    self.direction = inOut
    if self._guiCb:
      self._guiCb(self)
      
  def get(self):
    return self.state
    
    
class Gui:
  """create Gui in own thread"""
  running = 0
  cbClose = None
  pins = []
  gui = None
  
  def __init__(self, callback=None, cbClose=None, pins = None, maxPins=30):
    self.cbClose = cbClose
        
    self._gthread = _TGui(callback, self._cbGetGui, self._cbClose)
    self._gthread.start()

    time.sleep(0.1)
    
    if pins: 
      self.pins = pins
      self.maxPins = len(pins)
    else:
      self.maxPins = maxPins
      for i in range(maxPins):
        pins.append(Pin(i, _cbPin))
        
    for p in pins:
      self._genGuiPin(p.pinNum)
        
  def _cbClose(self):
    running = 0
    if self.cbClose:
      self.cbClose()
    
  def cbGetGui(self, gui):
    self.gui = gui
    self.running = 1
    
  def _genGuiPin(self,pinNum):
    l = self.gui.tk.Label(self.gui.win, "P"+str(pinNum))
    l.pack()
    self.gui.pins.append(l)
    
  def _getPin(self, pinNum):
    for pin in pins:
      if pin.pinNum == pinNum:
        return pin
    return None
    
  def _cbPin(self, pin):
    if not pin in self.pins: return
    gp = self.gui.pin[pin.pinNum]
    gp["text"] = str(pin.state)
    
      
  def getPinState(self, pinNum):
    p = self._getPin(pinNum)
    if p: return p.state
    return None
    
  def setPin(self, pinNum, hiLo):
    p=self._getPin(pinNum)
    if not p: return
    p.set(hiLo)
    
  def setPinDir(self, pinNum, inOut):
    p=self._getPin(pinNum)
    if not p: return
    p.setDir(hiLo)
    
  def setPinText(self, pinNum, text):
    return
    
    
    
class _TGui:
  pins = []
  
  def __init__(self, callback=None, cbGetGui=None, cbClose=None):
    self.cbGetGui = cbGetGui
    self.cbClose = cbClose
    self.callback = callback
    
    self.win = tk.Tk()
    self.tk = tk
    
    if self.cbGetGui:
      self.cbGetGui(self)
      
    self.win.mainloop()
    if cbClose:
      self.cbClose()

  def addPin(self, pinNum):
    l = self.tk.Label(self.win, "P"+str(pinNum))
    l.pack()
    self.pins.append(l)  

# - for test only -
def test():
  def cb1(*a,**k):
    return
    
  g = Gui(cb1)
  while(g.running):
    time.sleep(0.1)
  
  
if __name__ == "__main__":
  test()
  
#eof
