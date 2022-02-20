"""pins for wemos nodemcu v3"""

__version__ = "1.1.0"

import machine

pinLed = 2 #gpio2 = D4
pinBtn = 0

def getBtn():
  p0=machine.Pin(pinBtn,machine.Pin.IN)
  return p0.value()==0
  
def pwmLed():
  p2=machine.Pin(pinLed, machine.Pin.OUT)
  pw2=machine.PWM(machine.Pin(pinLed))
  return pw2
     
def ledOnOff(onOff):
  p2=machine.Pin(pinLed, machine.Pin.OUT)
  if onOff:
    p2.value(0)
  else:
    p2.value(1)
  
def adc(read16 = False):
  a=machine.ADC(0) # we've only this adc channel
  if read16:
    return a.read_u16()
  return a.read()

def gotodeepsleep(ms):
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  rtc.alarm(rtc.ALARM0,ms); machine.deepsleep()


# eof
