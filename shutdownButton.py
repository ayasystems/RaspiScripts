#Autor Angel / ayasystems
#
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

BUTTON_SHUTDOWN = 40#Setup with your GPIO Button

def goodbye():
    syslog.syslog("Closing script, good bye")
    GPIO.cleanup()           # clean up GPIO on normal exit

def button_shutdown(channel):
    global start
    global end
    if GPIO.input(BUTTON_SHUTDOWN) == 0:
        start = time.time()
#       print"pulsado"
    if GPIO.input(BUTTON_SHUTDOWN) == 1:
#        print"libre"
        end = time.time()
        elapsed = end - start
#        print(elapsed)
        if ( elapsed>2 and elapsed < 5):# entre 2 y 5 segundos
             syslog.syslog("Raising reboot command")
             os.system("sudo reboot now")
        if elapsed>=10:# mas de 10 segundos
             syslog.syslog("Raising shutdown command")
             os.system("sudo shutdown now")

#print("GPIO VERSION: " + str(GPIO.VERSION))
syslog.syslog("Shutdown button ->  GPIO: " + str(BUTTON_SHUTDOWN))
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_SHUTDOWN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
atexit.register(goodbye)

GPIO.add_event_detect(BUTTON_SHUTDOWN,GPIO.BOTH,callback=button_shutdown)
start = time.time()
end   = time.time()

#print(start)
#print(end)

while True:

    time.sleep(1)
