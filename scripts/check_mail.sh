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


