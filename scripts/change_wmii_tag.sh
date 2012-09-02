#!/bin/bash
#
# Script to change the current wmii tag
# Used primarily as a shortcut/alias.

if [ $# -lt 1 ]
then
    echo "Usage: $0 <tag>"
fi

wmiir xwrite /ctl view $1

