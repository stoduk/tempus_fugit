#!/bin/bash

# The i2c channel was switched for Model B from early boards (rev 2/3)
# from channel 0 to channel 1.  All other boards (including all Model A)
# use channel 1.

# Complication: for some reason my model B (rev 2) is returning a boardrev
# of 0x1000002 - the top bit being the overvolt bit (no idea why that is set
# as I haven't tried to do any overclocking!).  So need to just look at the
# bottom bits - but to get bitwise operations requires installing gawk
# rather than the standard awk which is mawk.

REVISION=`cat /proc/cmdline | gawk -v RS=" " -F= '/boardrev/ { print  and(strtonum($2), 0x0FFFFFF)  }'`

if [ "$REVISION" -eq "2" -o "$REVISION" -eq "3" ]; then
   echo 0;
else
   echo 1;
fi
