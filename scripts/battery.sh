#!/bin/bash
# script that gives notifications when battery is low
#
# TODO: only give notifications when battery discharging?  can be done by just
# looking at whether the perc is lower Do something diferent for when charging:
# Give indeication when started charging Give a notification when battery fully
# charged
#
# TODO: acpi returns bad data when it drops below 5%.  Jumps directly to 0%, so
# we'll end up skipping 3,2,1%, which are the most important ones.  Perhaps we
# should have more warning before 5% so that even if it skips the lower ones,
# we'll be garaunteed warnings.
#
# possible feature: unplugged/plugged notifications Notify user when the laptop
# is unplugged/plugged in. Might be annoying, but could be useful if user
# accidentally unplugs or starts up unintentionally unplugged (which I've done
# several times.)
#



# from my use, % changes every 1-2 minutes, so w/ 60 seconds, we'll get each % 1-3 times
SLEEP_TIME=60


# makes noise/beeps/etc
#  Use echo -e for \n's to work
make_noise()
{
    # TODO: may want to change sound level
    echo -e "$@" | espeak -a 200 &> /dev/null
}

prev="101"
while :
do
    # grabs the percentage (w/o the % or any other trailing stuff (i.e: the comma)
    perc=`acpi -b | awk '{print substr($4, 1, (index($4, "%")-1) )}'`

# for debugging
#    read perc

    # TODO: remove when done debugging
    echo "DEBUG: $perc"

    # decreasing
    if [ $perc -lt $prev ]
    then
        case $perc in
            "100")
                notify-send "battery $perc% (fully charged)"
                ;;
            "15")
                notify-send "battery $perc%"
                ;;
            "10")
                notify-send "battery $perc%"
                ;;
            "5")
                notify-send "battery $perc%"
                make_noise "battery is at $perc%"
                ;;
            "4")
                notify-send "battery $perc%"
                make_noise "battery is at $perc%"
                ;;
            "3")
                notify-send "battery $perc%"
                make_noise "battery is at $perc%"
                ;;
            "2")
                notify-send "battery $perc%"
                make_noise "battery is at $perc%"
                ;;
            "1")
                notify-send "battery $perc%"
                make_noise "WARNING\n battery is at $perc%"
                ;;
            "0")
                notify-send "battery $perc%"
                make_noise "WARNING\n battery is at $perc%"
                ;;
        esac
    fi

    # increasing
    if [ $perc -gt $prev ]
    then
        case $perc in
            "100")
                notify-send "battery $perc% (fully charged)"
                ;;
        esac
    fi


    prev=$perc
    sleep $SLEEP_TIME
done

