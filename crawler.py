from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
import datetime
import dateutil.parser
from enum import Enum
import calendar


class Crawler():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    
    def getEvents(self, clanedarId, startTime, endTime):
        # authentication
        store = file.Storage('token.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # get events
        events_result = service.events().list(
            calendarId=clanedarId,
            timeMin=startTime,
            timeMax=endTime,
            singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        myEvents = []

        # parse events
        for event in events:
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')
            startDate = dateutil.parser.parse(start)
            endDate = dateutil.parser.parse(end)    
            duration = endDate - startDate

            title = event['summary']

            splitTitle = title.split(' ')
            identification = splitTitle.pop(0)
            comment = ' '.join(splitTitle)
            projectId, storyNo = identification.split(':')

            myEvents.append({"projectId": projectId, "storyNo": storyNo, "comment": comment, "start": start, "end": end, "duration": duration})

        return myEvents

 
    def getToday(self, calendarId):
        startTime = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0)
        startTime = startTime.isoformat() + 'Z'

        endTime = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59)
        endTime = endTime.isoformat() + 'Z'
        return self.getEvents(calendarId, startTime, endTime)


    def getWeek(self, calendarId, week=0, year=datetime.date.year):
        if week == 0:
            startTime = datetime.datetime.utcnow()
            weekDay = startTime.weekday() # mo = 0, so = 6
            startTime = startTime - datetime.timedelta(weekDay) #set to monday
            startTime = startTime.replace(hour=0, minute=0)
            
            endTime = startTime + datetime.timedelta(6) # + 6 days to get SO
            endTime = endTime.replace(hour=23, minute=59)
            startTime = startTime.isoformat() + 'Z'
            endTime = endTime.isoformat() + 'Z'

            return self.getEvents(calendarId, startTime, endTime)
        else: 
            days = week * 7
            endTime = datetime.datetime.utcnow().replace(month=1, day=1, hour=23, minute=59)
            endTime = endTime + datetime.timedelta(days)
            startTime = endTime - datetime.timedelta(6) # - 6 days
            startTime = startTime.isoformat() + 'Z'
            endTime = endTime.isoformat() + 'Z'

            return self.getEvents(calendarId, startTime, endTime)
            



    def getMonth(self, calendarId, month=datetime.date.today().month, year=datetime.date.today().year):
        startTime = datetime.datetime.utcnow().replace(year=year, month=month, day=1, hour=0, minute=0, second=0)
        startTime = startTime.isoformat() + 'Z'
            
        noOfDays = calendar.monthrange(year, month)[1]
        endTime = datetime.datetime.utcnow().replace(year=year, month=month, day=noOfDays, hour=23, minute=59, second=59)
        endTime = endTime.isoformat() + 'Z'

        return self.getEvents(calendarId, startTime, endTime)


    def getYear(self, calendarId, year=datetime.date.today().year):
        startTime = datetime.datetime.utcnow().replace(year=year, month=1, day=1, hour=0, minute=0, second=0)
        startTime = startTime.isoformat() + 'Z'

        endTime = datetime.datetime.utcnow().replace(year=year, month=12, day=31, hour=23, minute=59, second=59)
        endTime = endTime.isoformat() + 'Z'
        
        return self.getEvents(calendarId, startTime, endTime)


    def getTimeFrame(self, calendarId, startYear, startMonth, startDay, startHour, startMinute, startSecond, 
                    endYear, endMonth, endDay, endHour, endMinute, endSecond):

        startTime = datetime.datetime.utcnow().replace(year=startYear, month=startMonth, day=startDay, 
                    hour=startHour, minute=startMinute, second=startSecond)
        startTime = startTime.isoformat() + 'Z'

        endTime = datetime.datetime.utcnow().replace(year=endYear, month=endMonth, day=endDay, 
                    hour=endHour, minute=endMinute, second=endMinute)
        endTime = endTime.isoformat() + 'Z'

        return self.getEvents(calendarId, startTime, endTime)

