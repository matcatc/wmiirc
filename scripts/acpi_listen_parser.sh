#!/bin/bash
# watches acpi_listen, and calls appropriate scripts based on what it sees
#
# b/c acpi_fakekey and related wasn't working for me.
# Plus, this is simpler.
#
# Note: b/c this is run daemonically, the keys will work while the screen is
# locked. I actually like this originally unintended behavior, so I left it as
# is.

DEBUG=0

# allows us to switch volume status scripts in one location
volume_status()
{
    ~/.wmii/scripts/pulse_system_volume_status.py
}



acpi_listen |
while read description command id1 id2
do
    if [ $DEBUG -eq 1 ]
    then
        echo "description = $description"
        echo "command = $command"
        echo "id1 = $id1"
        echo "id2 = $id2"
    fi

    case $command in
        "MUTE")
            echo "muting"
            ~/bin/mute_volume.sh > /dev/null
            volume_status
            ;;
        "VOLDN")
            echo "vol down"
            ~/bin/lower_volume.sh > /dev/null
            volume_status
            ;;
        "VOLUP")
            echo "vol up"
            ~/bin/raise_volume.sh > /dev/null
            volume_status
            ;;
        "CDPLAY")
            echo "play/pause"
            mpc toggle > /dev/null
            ;;
        "CDSTOP")
            echo "stop"
            mpc stop > /dev/null
            ;;
        "CDPREV")
            echo "prev"
            mpc prev > /dev/null
            ;;
        "CDNEXT")
            echo "next"
            mpc next > /dev/null
            ;;
    esac

done

