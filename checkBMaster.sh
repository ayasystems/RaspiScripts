#!/bin/bash
scriptpath=/home/pi/scripts
scriptlog=/home/pi/scripts
url="http://master.brandmeister.es/checkclient.php?callID=ED4ZAI"

status_code=$(curl  --silent   $url)

date=`date`
scriptlog+="/status_check.log"
if [ $status_code != "connected" ]
then
		echo "status check failed at $date"
        echo "status check failed at $date" >> $scriptlog
		#You can add further actions here
		sudo systemctl stop mmdvmhost
		sudo systemctl start mmdvmhost
fi
