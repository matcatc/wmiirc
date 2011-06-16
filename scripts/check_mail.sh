#!/bin/bash

#notify-send "Debug: calling check_mail script"

SLEEP_TIME=10s


echo -n 'Mail: starting' | wmiir create /rbar/mail
while :
do

        if ps -A | grep 'claws-mail' > /dev/null
        then
            echo -n 'Mail: ' $(claws-mail --status) | wmiir write rbar/mail
        else
            echo -n 'Mail: N/A' | wmiir write rbar/mail
        fi

        sleep $SLEEP_TIME
done


