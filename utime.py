# dummy lib
"""
dummy library - to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

from time import *

# consts
__version__ = "0.1.0.0"

MAX_VALUE = (1<<32)-1
TIME_20220801 = 1659295000

def ticks_ms():
  return int((time()-TIME_20220801) * 1000) 
  
def ticks_diff(a,b):
  d = a-b;
  if d<0:
    d += MAX_VALUE
  return d;

#eof
