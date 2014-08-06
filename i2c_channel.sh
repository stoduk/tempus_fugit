#!/bin/bash

# The i2c channel was switched for Model B from early boards (rev 2/3)
# from channel 0 to channel 1.  All other boards (including all Model A)
# use channel 1.
REVISION=`cat /proc/cmdline | awk -v RS=" " -F= '/boardrev/ {print int($2)}'`

if [ "$REVISION" -eq "2" -o "$REVISION" -eq "3" ]; then
   echo 0;
else
   echo 1;
fi
