#!/bin/bash
#Recibe como argumento el texto a reproducir
#Es necesario estar registrado en http://www.voicerss.org/
#Desde nuestros scripts de domoticz llamamos a este script pasando como argumento el texto a reproducir

#echo $*
url="http://api.voicerss.org/?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&f=48khz_16bit_mono&hl=es-es&src="$*
#echo $url
#si existe /tmp/voice.pid esperamos a que no exista. Puede que esté reproduciendo algo en este momento
until [ ! -f /tmp/voice.pid ]
do
     sleep 5
done
touch /tmp/voice.pid
wget -O /tmp/speech.mp3 "${url}" -q 2>&1
mpg123 -a hw:1,0 /tmp/speech.mp3  >/dev/null 2>&1
rm /tmp/voice.pid
