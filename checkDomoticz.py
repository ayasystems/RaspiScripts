#!/usr/bin/python
#Script para reiniciar domoticz cuando se detecta que este deja de responder a peticiones HTTP
#ajuste la URL según sus necesidades.


import json
import urllib
import time
import sys
import os
def checkDomoticz():
    url = 'http://localhost/json.htm?type=command&param=getversion'
    try:
      output = json.load(urllib.urlopen(url))
    except ValueError:
      return 0
    except IOError, e:
      return 0
    if 'status' not in output:
      #raise ValueError("No target in given data")
      return 0
    else:
      return 1
if(checkDomoticz()==1):
   print("Domoticz funciona")
   sys.exit(0)
#no funciona, esperamos 5 segundos y probamos de nuevo
print("Domoticz ha fallado una vez")
time.sleep(5)
if(checkDomoticz()==1):
   print("Domoticz funciona")
   sys.exit(0)
print("Domoticz ha fallado dos veces, recinicio el servicio")
#no funciona, reiniciamos el servicio
print("Ejecutando sudo systemctl stop domoticz")
os.system("sudo systemctl stop domoticz")
print("Ejecutando sudo systemctl start domoticz")
os.system("sudo systemctl start domoticz")
sys.exit(0)


