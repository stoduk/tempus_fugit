Raspberry Pi time lapse daemon

Designed to be run at startup on a Raspberry Pi running a MoPi power
monitor - such that we will be started once the RPi is up and running,
we'll do our work, and then ask MoPi to turn RPi off and wake up again
later.  Much like a hardware cron job.

This is designed with a network-unattahed RPi model A running off batteries
- this will give the longest possible battery life for our time lapse, but
to get sane dates on the photos we'll want a hardware RTC connected too.

The device is likely to be run remotely to the person who knows how to fix
it, so the aim is that everything can be run without needing an attached
monitor or any great intelligence.  The device will snap pictures away
at the configured times, and when a USB drive is plugged in it will update
itself and copy off any photos taken.  Nice and simple.

The work to do on each power up is:
- if a USB drive is found, copy over any new configuration
 (this is useful as we are running remotely and not network connected)
- take a photo!
- if a USB drive is found, copy off any photos and log files (eg. to
 indicate power state)

