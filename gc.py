# dummy lib
"""
dummy library gc to emulate esp8266 micropython on a PC with python3
uncomplete
2022 by lifesim.de
"""

from gc import *

def mem_alloc():
  return 1000
  
def mem_free():
  return -1

def threshold(a):  
  return -1
  
#eof
