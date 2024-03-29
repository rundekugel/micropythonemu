#!/usr/bin/env python3
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
__version__ = "0.2.0.0"

#self for one instace
obj = None

# classes 
class Pin:
  """pin emulator"""
  DIRECTION_IN = 0
  DIRECTION_OUT = 1
  IRQ_FALLING = 2
  IRQ_RISING = 1
  state = 0
  direction = 0 
  _guiCb = None
  pinnum = None
  irq = None
  callback = None
  
  def __init__(self, pinnum, guiCb=None):
    self.pinnum=pinnum
    if guiCb: self._guiCb = guiCb
    
  def set(self,hiLo):
    if self.state == hiLo: return
    self.state = hiLo
    if self.irq and self.callback:
      rs = [self.IRQ_RISING, self.IRQ_FALLING][hiLo==0]
      if self.irq & rs:
        self.callback(self.pinnum)
      
  def setDir(self,inOut):
    if self.direction == inOut: return
    self.direction = inOut
    # ~ if self._guiCb:
      # ~ self._guiCb(self)
      
  def get(self):
    return self.state


class Gui:
  """create a Gui. Don't forget to call update repaetedly"""
  running = 0
  cbClose = None
  pins = []
  gui = None
  blockoutpins = True

  def __init__(self, callback=None, cbClose=None, pins=None, maxPins=10):
    self.cbClose = cbClose

    #self._gthread = threading.Thread(target=_TGui, args=(callback, self._cbGetGui, self._cbClose))
    #self._gthread.start()
    self.gui = _TGui(callback, self._cbGetGui, self._cbClose)
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
        self.pins.append(Pin(i))
        
    for p in self.pins:
      self._genGuiPin(p.pinnum)

    self._refreshallGuiPins()
        
  def _cbClose(self):
    self.running = 0
    # del self._gthread
    if self.cbClose:
      self.cbClose()
    del self
    
  def _cbGetGui(self, gui):
    self.gui = gui
    self.running = 1
    
  def _genGuiPin(self,pinnum):
    self.gui.addPin(pinnum, self._cbPinGui, self._cbPinGuiDir)

  def _getPin(self, pinnum):
    for pin in self.pins:
      if pin.pinnum == pinnum:
        return pin
    return None

  def _refreshGuiPin(self, pin):
    """read vals from pin and write to gui"""
    if not pin in self.pins: return
    if not self.running: return
    if not self.gui.isAlive():
      self.running = 0
      return
    try:
      gp = self.gui.pins[pin.pinnum]
      gp["text"] = str(pin.pinnum)
      if self.blockoutpins:
        gp["state"] = ["normal", "disabled"][pin.direction]
      gp.var.set(pin.state)
      gp.dir.set(pin.direction)
      gp.d["text"]= ["i", "o"][pin.direction]
    except:
      pass
  def renamePin(self, pinnum, text):
    if pinnum < self.maxPins: return
    gp = self.gui.pins[pinnum]
    gp["text"] = str(text)
    
  def _cbPinGui(self, pin=None):
    """write gui vals to pins"""
    self._refreshallpins()
    return
    #  todo: the following lines need parameter in callback
    # if not pin in self.pins: return
    # gp = self.gui.pin[pin.pinnum]
    # gp["text"] = str(pin.state)

  def _cbPinGuiDir(self):
    self._refreshallpins()

  def _refreshallpins(self):
    """read values from gui and write to pins"""
    for p in self.pins:
      state = self.gui.pins[p.pinnum].var.get()
      p.set(state)
      p.direction = self.gui.pins[p.pinnum].dir.get()
      self._refreshGuiPin(p)
      
  def _refreshallGuiPins(self):
    for p in self.pins:
      self._refreshGuiPin(p)

  def getPinState(self, pinnum):
    if not self.running: return None
    p = self._getPin(pinnum)
    if p: return p.state
    return None
    
  def setPin(self, pinnum, hiLo):
    p=self._getPin(pinnum)
    if not p: return
    p.set(hiLo)
    self._refreshGuiPin(p)
    
  def setPinDir(self, pinnum, inOut):
    p = self._getPin(pinnum)
    if not p:  return
    p.setDir(inOut)
    self._refreshGuiPin(p)

  def setPinText(self, pinnum, text):
    self.renamePin(pinnum,text)

  def setIrq(self, handler=None, pinnum=0, irqtype=Pin.IRQ_RISING|Pin.IRQ_FALLING):
    p=self._getPin(pinnum)
    if not p: return
    p.irq = irqtype
    p.callback = handler
    
  def getAdc(self, id=0):
    """adc emulator for esp8266."""
    v=-1
    try:
      t = self.gui.adcs[0].get()
      v = int(t,0)
    finally:
      return v


class _TGui:
  pins = []
  running=0
  width = 400
  height = 110
  adcs = []

  def __init__(self, callback=None, cbGetGui=None, cbClose=None):
    self.cbGetGui = cbGetGui
    self.cbClose = cbClose
    self.callback = callback
    
    self.win = tk.Tk()
    self.win.geometry("%ix%i"%(self.width, self.height))
    self.tk = tk

    l= tk.Label(self.win, text="ADC0:")
    l.place(relx=.01, rely=.75)
    ed = tk.Entry(self.win)
    ed.place(relx=.13, rely=.75)

    self.adcs.append(ed)

    if self.cbGetGui:
      self.cbGetGui(self)
    self.running = 1
    return
    # self.win.mainloop()
    self.running =0
    if cbClose:
      self.cbClose()

  def isAlive(self):
    return not not self.win.children

  def update(self):
    if self.running:
      if not self.win.children:
        self.running = 0
        if self.cbClose:
          self.cbClose()
        return False
      self.win.update()
      return True
    else:
      if self.cbClose:
        self.cbClose()

  def stop(self):
    self.running = 0
    self.win.quit()

  def addPin(self, pinnum, cb=None, cbDir=None):
    var=tk.IntVar()
    o = tk.Checkbutton(self.win, variable=var, text=str(pinnum), command=cb)
    o.grid(row=2, column=pinnum)
    o.var = var
    dir = tk.IntVar()
    o.d = tk.Checkbutton(self.win, variable=dir, text="i", command=cbDir)
    o.d.grid(row=3, column=pinnum)
    o.dir = dir
    self.pins.append(o)
    return

# - for test only -
def test():
  """halEmu demo"""
  print("halEmu demo")
  print("use pin9 to stop or <ctrl>+<C> or just close the window") 
  def cb1(*a,**k):
    """demo pin irq"""
    print(a,k)
    return

  g = Gui(cb1)
  g.setPin(2,1)
  g.setIrq(cb1, 4, Pin.IRQ_RISING)
  s=g.getPinState(3)
  valueAdc = None
  while(g.running):
    if g.getPinState(9):  # pin 9 stops script
      g.gui.stop()
    # repeatedly update needed  
    if not g.gui.update():
      break
    # demo show pin state  
    s2=g.getPinState(3)
    if s!=s2:
      print("pin3 changed to %i."%s2)
      s=s2
    # demo change pin from program  
    s7=g.getPinState(7)
    g.setPin(7, 1-s7)
    # demo adc
    vadc = g.getAdc()
    if valueAdc != vadc:
      print("ADC changed from %s to %i"%(str(valueAdc),vadc))
      valueAdc = vadc 
      
    time.sleep(0.1)
  time.sleep(0.5)
  print("bye.")
  del g


if __name__ == "__main__":
  test()
  
#eof
