#!/bin/bash
# watches acpi_listen, and calls appropriate scripts based on what it sees
#
# b/c acpi_fakekey and related wasn't working for me.
# Plus, this is simpler.

DEBUG=0


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
            ~/.wmii/scripts/alsa_volume_status.py
            ;;
        "VOLDN")
            echo "vol down"
            ~/bin/lower_volume.sh > /dev/null
            ~/.wmii/scripts/alsa_volume_status.py
            ;;
        "VOLUP")
            echo "vol up"
            ~/bin/raise_volume.sh > /dev/null
            ~/.wmii/scripts/alsa_volume_status.py
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

