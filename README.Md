## Google Calendar on e-Ink display
This project uses a Waveshare 7.5" E-Ink display ( https://www.robotshop.com/en/640x384-75-e-ink-display-hat-raspberry-pi.html ) and a Raspbery Pi 0 Wireless ( https://www.raspberrypi.org/products/raspberry-pi-zero-w/ ) along with some easy Python code to make a Google Calendar for your home.

In my family's case, we need a common calendar to keep up with After School Activities, appointments, etc. We set up a shared Google Calendar, but certain teen... er, *members* of our family kept muting the notifications on their phone, and saying, "I didn't see that on the calendar!"

Now we have a lovely shadowbox picture frame - conveniently beside the TV - for everyone to see the schedule!

This is a pretty easy build, and if you get the Pi0W pre-built with headers (available from some resellers) you don't even have to solder anything!

The Python program here will download your calendar and print it to the e-Ink display!

## Caveat:
I used the version 1 Waveshare display (640 x 384 resolution), and the current version has a higher resolution. That means my line spacing will work, but won't use all of the screen. Look at the maxResults variable and the l (line spacing) variable, and tune them to your heart's content.

## Getting Started 
Start with a Raspberry Pi or Raspberry Pi 0 (way cheaper) with the latest version of Raspbian. There are multiple variations on Raspbian now, so to make certain you have all the necessary libraries, etc., you can just start with the full desktop version.

The Waveshare board requires the SPI interface to be enabled on the Pi. If you're not sure how to do that, check out the guide here: https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

### Dependencies
I make use of Pandas dataframes and timezone conversion from pytz, so you must:
```
pip install pandas pytz
```
In the code, the lines:
```
  eastern = pytz.timezone('US/Eastern')
 ...
          start = pytz.utc.localize(start, is_dst=None).astimezone(eastern)
```
should be changed to your time zone.

Obviously, you need a Google Calendar (an exercise left to the reader). You will also need to create a credentials.json file from your Google Calendar into the python directory to give Python access to the service. The instructions for that are here:
https://developers.google.com/calendar/quickstart/python

This tutorial will walk you through some of the Python dependencies, such as:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Notice the sample Python code there is the basis for this code - altered to print to an e-ink display, rather than the console.

As you go through the tutorial, find the place in the calendar.py code here where it says `events_result = service.events().list(calendarId='<insert your calendarID from google>'` and change the calendarID to the one you create in the tutorial.

The e-ink display from Waveshare has its own Python code, and requires the Pillow library:
```
pip install --upgrade Pillow
```
You will also need to download their sample repository ( https://github.com/soonuse/epd-library-python/tree/master/7.5inch_e-paper ) and copy the epdif.py and epd7in5.py files into the directory where you have downloaded this Python script.

## The Build
The e-Ink display has a "hat" to fit onto the header of the Pi, and a ribbon cable to connect the hat to the display - that's it! I put mine in a nice shadowbox, and cut black paper to serve as a frame around the screen. You can see the pictures in the images directory.

Clone the repo to your Raspberry Pi, preferably into the home directory (after following all of the instructions above, of course). From the terminal, `cd `into the python directory (where you have copied all of the files mentioned in dependencies above) and 
type:
`python calendar.py`

If your default python is python 2.7, you may need to specify:

`python3 calendar.py`

### Chron task
I also set up a chron task to run the script once an hour. You may want to run it more often or less often. Follow the instructions here for help:
 
https://www.raspberrypi.org/documentation/linux/usage/cron.md

*Note*: Because of the dependencies, you will need to add `cd <PATH>/python &&` before you call Python 3 with the script name (as above), where `<PATH>` is wherever you saved the repository (e.g., /home/pi).

an example might be:
```
crontab -e
# Insert into crontab:
0 5-11 * * *  cd /home/pi/python && python calendar.py
# save and exit
```
The above would set the job to run from 5AM until 11AM every hour

### If your display quality begins to degrade (IMPORTANT)
After some months I noticed my display fading, to fix it I have now updated the code to put the display to sleep after each update, and changed my chron job to call the main.py file included nightly.
This update causes the screen to go BLACK at night, and the results are fantastic! Right back to crisp, black letters.

My chrontab looks like this now:
```
0 6-20/2 * * * cd /home/pi/calendar/ && python3 calendar.py
0 21 * * * cd /home/pi/calendar/ && python3 main.py
```

This updates only every two hours between 6AM and 8PM, and blacks out the screen at night.

