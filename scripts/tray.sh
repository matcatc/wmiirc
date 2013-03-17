#!/bin/bash

# TODO: redirect output based on command line argument
#  /dev/null vs stdout?

# kill previous instance of trayer
killall trayer
sleep 1
killall -9 trayer

# start trayer
trayer --SetPartialStrut true --edge right --height 100
