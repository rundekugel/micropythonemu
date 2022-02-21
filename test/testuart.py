"""
test pin, uart and adc ESP8266 emulation
pin0 is used as button
"""
import sys
sys.path.append("..")
import uos as os
import machine
import board_nm3 as board
import time
from machine import ADC

# consts
__version__ = "0.1.0.0"

def reattach():
  uart = machine.UART(0, 115200)
  os.dupterm(uart, 1)
  
def detach():
  os.dupterm(None, 1)  
  
def u1():
  detach()
  if not machine.ismicropython:
    # machine.UART.port = "/dev/tty"
    machine.UART.port = "/dev/ttyUSB0"  # Linux
    # machine.UART.port = "com31"   # Windows
  u=machine.UART(0,baudrate=115200, timeout=500)
  u.write("?"+os.linesep)
  doit=1
  while doit:
    r=u.readline()
    if r:
      print(">",r)
      u.write(r)
      a=getad()
      u.write(str(a))
    if r==b"Q":
      doit=0
  reattach()

def getad():
  doit =1
  ad=ADC(0)
  while doit:
    print(ad.read())
    time.sleep(0.1)
    if board.getBtn()==0:
      doit=0

if __name__ == "__main__":
  u1()

#eof