#!/bin/bash


# use gnome-screensaver is running
if [ $(pidof 'gnome-screensaver') ]
then
    echo 'gnome-screensaver-command --lock'
    gnome-screensaver-command --lock

# use xscreensaver otherwise
else
    # start xscreensaver if necessary
    if [ ! $(pidof 'xscreensaver') ]
    then
        echo 'starting xscreensaver'
        xscreensaver &
    fi

    echo 'xscreensaver-command -lock'
    xscreensaver-command -lock
fi

