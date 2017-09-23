#Autor Angel EA4GKQ
# 
#
import syslog
import time
import RPi.GPIO as GPIO
import atexit
import os
var = 1
counter = 0
global start
global end

try:
    import httplib
except:
    import http.client as httplib


BUTTON_SHUTDOWN = 40 #Setup with your GPIO Button
LED_PIN         = 38 

def have_internet():
#    conn = httplib.HTTPConnection("www.google.com", timeout=5)
#    try:
#        conn.request("HEAD", "/")
#        conn.close()
#        return True
#    except:
#        conn.close()
#        return False
	status_eth0  = open('/sys/class/net/eth0/operstate', 'r').read()
	status_wlan0 = open('/sys/class/net/wlan0/operstate', 'r').read()
#	print(status_eth0)
#	print(status_wlan0)
	if(status_eth0 != 'down' or status_wlan0 != 'down'):
		return True
	else:
		return False

def goodbye():
    syslog.syslog("Closing script, good bye")
    GPIO.cleanup()           # clean up GPIO on normal exit

def button_shutdown(channel):
    global start
    global end
    if GPIO.input(BUTTON_SHUTDOWN) == 0:
        start = time.time()
#        print("pulsado")
    if GPIO.input(BUTTON_SHUTDOWN) == 1:
#        print("libre")
        end = time.time()
        elapsed = end - start
        print(elapsed)
        if ( elapsed>0.2):# Pulsacion mayor a 0.2 segudos (evita rebotes/ruido)
             syslog.syslog("Raising shutdown command")
             os.system("sudo shutdown now")
#             print("shutdown <10")
print("GPIO VERSION: " + str(GPIO.VERSION))
syslog.syslog("Shutdown button ->  GPIO: " + str(BUTTON_SHUTDOWN))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_SHUTDOWN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT) 
atexit.register(goodbye)

GPIO.add_event_detect(BUTTON_SHUTDOWN,GPIO.BOTH,callback=button_shutdown)
start = time.time()
end   = time.time()


while True:

    time.sleep(0.1)
    if( have_internet()):
	GPIO.output(LED_PIN,True)
	time.sleep(0.1)
	GPIO.output(LED_PIN,False)
    else:
        GPIO.output(LED_PIN,False)
