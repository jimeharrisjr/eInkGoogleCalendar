from __future__ import print_function
import datetime
import pickle
import os.path
import pytz
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import epd7in5
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import imagedata

EPD_WIDTH = 640
EPD_HEIGHT = 384

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    epd = epd7in5.EPD()
    epd.init()
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 18 events')
    events_result = service.events().list(calendarId='family11085102172024106957@group.calendar.google.com', timeMin=now,
                                        maxResults=18, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    eastern = pytz.timezone('US/Eastern')
    lst=[]
    time = ' '
    date=' '
    what=' '
    cols=['day','date','time','what']
    if not events:
        print('No upcoming events found.')
    for event in events:
        #print(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        time = ' ' 
        date=' '
        what=' '

        if (start.find('T') != -1):
          #print(start)
          start =datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
          start = pytz.utc.localize(start, is_dst=None).astimezone(eastern)
          day = start.strftime('%A')
          date = start.strftime('%B %d')
          time = start.strftime('%I:%M %p')
          what=event['summary']
        #print(date,time,what)
        lst.append([day,date,time,what])

    df=pd.DataFrame(lst,columns=cols)
    n=df['date'].count()
    a=[1]*(n)
    for i in range(0,n-1):
        x=i+1
        #(df['day'][i],df['day'][x])
        if df['day'][i] != df['day'][x]:
            a[x]=0
    df['num']=a
    n=df['date'].count()
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 16)
    draw.text((10, 5), df.iloc[0,0], font = font, fill = 0)
    draw.text((110, 5), df.iloc[0,1], font = font, fill = 0)
    draw.text((220, 5), df.iloc[0,2], font = font, fill = 0)
    draw.text((300, 5), df.iloc[0,3], font = font, fill = 0)
    l=2
    for i in range(1,n-1):
        if df['num'][i]==1:
            l=l+20
            draw.text((220, l), df.iloc[i,2], font = font, fill = 0)
            draw.text((300, l), df.iloc[i,3], font = font, fill = 0)
            


        else:
            l=l+22
            draw.line((10,l,630,l), fill=0)
            l=l+2
            draw.text((10, l), df.iloc[i,0], font = font, fill = 0)
            draw.text((110, l), df.iloc[i,1], font = font, fill = 0)
            draw.text((220, l), df.iloc[i,2], font = font, fill = 0)
            draw.text((300, l), df.iloc[i,3], font = font, fill = 0)
            
                
    epd.display_frame(epd.get_frame_buffer(image))
                
      

if __name__ == '__main__':
    main()
