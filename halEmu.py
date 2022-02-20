# dummy lib
"""
library to emulate esp8266 hardware for micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

import machine
import tkinter as tk
import time
import threading

# consts

# classes 
class Pin:
  """pin emulator"""
  DIRECTION_IN = 0
  DIRECTION_OUT = 1
  state = 0
  direction = 0 
  _guiCb = None
  pinnum = None
  
  def __init__(self, pinnum, guiCb=None):
    self.pinnum=pinnum
    if guiCb: self._guiCb = guiCb
    
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
  """create a Gui in it's own thread"""
  running = 0
  cbClose = None
  pins = []
  gui = None
  
  def __init__(self, callback=None, cbClose=None, pins = None, maxPins=10):
    self.cbClose = cbClose
        
    self._gthread = threading.Thread(target=_TGui, args=(callback, self._cbGetGui, self._cbClose))
    self._gthread.start()

    timeout=9
    while(timeout):
      timeout-=1
      time.sleep(0.1)
      if self.running:
        break
    
    if pins: 
      self.pins = pins
      self.maxPins = len(pins)
    else:
      self.maxPins = maxPins
      for i in range(maxPins):
        self.pins.append(Pin(i, self._cbPin))
        
    for p in self.pins:
      self._genGuiPin(p.pinnum)
        
  def _cbClose(self):
    self.running = 0
    if self.cbClose:
      self.cbClose()
    
  def _cbGetGui(self, gui):
    self.gui = gui
    self.running = 1
    
  def _genGuiPin(self,pinnum):
    self.gui.addPin(pinnum, self._cbPinGui)

  def _getPin(self, pinnum):
    for pin in self.pins:
      if pin.pinnum == pinnum:
        return pin
    return None

  def _cbPin(self, pin=None):
    if not pin in self.pins: return
    gp = self.gui.pins[pin.pinnum]
    gp["text"] = "P:%s=%i Dir=%s"%(str(pin.pinnum),
                  (pin.state),["in","out"][pin.direction])
    gp["state"]=["disabled","normal"][pin.direction]
    gp.var.set( pin.state)

  def renamePin(self, pinnum, text):
    if pinnum < self.maxPins: return
    gp = self.gui.pins[pinnum]
    gp["text"] = str(text)
  def _cbPinGui(self, pin=None):
    self.refreshallpins()
    if not pin in self.pins: return
    gp = self.gui.pin[pin.pinnum]
    gp["text"] = str(pin.state)
  def refreshallpins(self):
    for p in self.pins:
      p.state = self.gui.pins[p.pinnum].var.get()
  def getPinState(self, pinnum):
    p = self._getPin(pinnum)
    if p: return p.state
    return None
    
  def setPin(self, pinnum, hiLo):
    p=self._getPin(pinnum)
    if not p: return
    p.set(hiLo)
    
  def setPinDir(self, pinnum, inOut):
    p=self._getPin(pinnum)
    if not p: return
    p.setDir(hiLo)

  def setPinText(self, pinnum, text):
    return
    
    
    
class _TGui:
  pins = []
  running=0

  def __init__(self, callback=None, cbGetGui=None, cbClose=None):
    self.cbGetGui = cbGetGui
    self.cbClose = cbClose
    self.callback = callback
    
    self.win = tk.Tk()
    self.win.geometry("300x200")
    self.tk = tk
    
    if self.cbGetGui:
      self.cbGetGui(self)
    self.running = 1

    self.win.mainloop()
    self.running =0
    if cbClose:
      self.cbClose()

  def addPin(self, pinnum, cb=None):
    # l = self.tk.Label(self.win, text="P"+str(pinnum))
    # l = self.tk.Checkbutton(self.win, text=str(pinnum), variable=var1).grid(row=0, sticky=W)
    #o = self.tk.Checkbutton(self.win, text=str(pinnum), command=cb)
    var=tk.IntVar()
    o = tk.Checkbutton(self.win, variable=var,text=str(pinnum), command=cb)
    o.pack(side=tk.LEFT)
    o.var = var
    self.pins.append(o)
    return

# - for test only -
def test():
  def cb1(*a,**k):
    return
    
  g = Gui(cb1)
  g.setPin(2,1)
  s=g.getPinState(3)
  while(g.running):
    time.sleep(0.1)
    s2=g.getPinState(3)
    if s!=s2:
      print("pin3 changed to %i."%s2)
      s=s2
  
if __name__ == "__main__":
  test()
  
#eof
