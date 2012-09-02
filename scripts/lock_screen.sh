#!/bin/bash
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Matthew Todd

status=1

# use gnome-screensaver if running
if [ $(pidof 'gnome-screensaver') ]
then
    echo 'gnome-screensaver-command --lock'
    gnome-screensaver-command --lock
    status=$?

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
    status=$?
fi


# switch to a nother tag
if [ $status -eq 0 ]
then
    wmiir xwrite /ctl view lock
fi

