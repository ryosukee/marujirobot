#! /bin/bash
ping -c 1 192.168.0.1 >> /dev/null 2>> /dev/null
if [ $? == 0 ];
then
    :
else
    shutdown -r
fi
