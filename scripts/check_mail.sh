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


echo -n 'Mail: starting' | wmiir create /rbar/90-mail
while :
do
        status=$(claws-mail --status)

        # the below comparison is what claws-mail prints out when its not
        # running. Using this rather than grepping ps output b/c that'll fail
        # if it catches a previous grep. Ie: this script was previously
        # interfering with itself when the `claws-mail --status` process was
        # found. Plus this does one less subprocess call.
        if [ "$status" == '0 Claws Mail not running.' ]
        then
            echo -n 'Mail: N/A' | wmiir write rbar/90-mail
        else
            echo -n "Mail: $status" | wmiir write rbar/90-mail
        fi

        sleep $SLEEP_TIME
done


