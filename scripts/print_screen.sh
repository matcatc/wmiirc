#!/bin/bash
# simple script which does a screen shot and drops the image in the user's directory

scrot -e 'mv $f ~/ ; notify-send "file saved: $f"'
