"""
Convert a string to a python datetime.

Below are sample inputs that should work once everyting is done.

- absolute dates
may10

- absolute days and times
wednesday
wed
tomorrow
wednesday9am
tomorrow9am
9am

- relative
1h
1hour
2hours
1d
1day
2days
1w
1week
1weeks
1m
1month
1months
1year
1y
1years
- any combination of the above

"""

import re
import datetime
from dateutil.relativedelta import relativedelta

relativeRegex = r'''
    ^
    (?P<number>\d+)                                                 # number of days/months/...
    (?P<type>year|y|month|m|week|w|day|d|hour|h|minute|min)         # days/months/...
    s?                                                              # accept day or days
    (?P<remainingString>.*)                                         # will be searched recursively
    $
    '''
dayRegex = r'''
    ^
    (?P<day>monday|mon|tuesday|tue|wednesday|wed|thursday|thu|friday|fri|saturday|sat|sunday|sun|tomorrow|today)     # either weekday or tomorrow, optional
    (?P<time>\d{1,2}(?:am|pm|h)|)                                                                               # 9pm same as 21h, optional
    $
    '''
dateRegex = r'''
    ^
    (?P<month>jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)     # month
    (?P<day>\d{1,2})                                                                               # day of the month
    $
    '''

# return test from test@example.com, does not check if the string is a valid email address
def getEmailRecipient(emailAdress):
    matchObj = re.match(r'([^@]+)@', emailAdress)
    if matchObj:
        return matchObj.group(1)
    return None

def relativeTimeInString(timeString):
    # recursively extract relative time data from string, returns list of tuples like [(2, 'months')]
    relMatches = re.match(relativeRegex, timeString, re.VERBOSE)
    if relMatches:
        return [relMatches.group('number', 'type')] + relativeTimeInString(relMatches.group('remainingString'))
    return []

def addRelativeTime(amount,timeType,startTime=None):
    if not startTime:
        startTime = datetime.datetime.now()
    amount = int(amount)
    if timeType in ('year','y'):
        timeType = 'years'
    if timeType in ('month','m'):
        timeType = 'months'
    if timeType in ('week', 'w'):
        timeType = 'weeks'
    if timeType in ('day', 'd'):
        timeType = 'days'
    if timeType in ('hour', 'h'):
        timeType = 'hours'
    if timeType in ('minute', 'min'):
        timeType = 'mintues'
    return startTime + relativedelta(**{timeType:amount})

def relativeDateTimeFromTuples(timeTuples):
    targetTime = datetime.datetime.now()
    for amount, timeType in timeTuples:
        targetTime = addRelativeTime(amount, timeType, targetTime)
    return targetTime



def checkStringForTime(timeString):
    # everything is case-insensitive
    timeString = timeString.lower()
    # check for dates of type 'march30'
    dateMatch = re.match(dateRegex, timeString, re.VERBOSE)
    if dateMatch:
        print 'date: %s %s' % dateMatch.group('month', 'day')
        return
    # check for relative time of type '1year2months'
    relTime = relativeTimeInString(timeString)
    if relTime:
        print 'relative: ', relTime
        print 'time: ', relativeDateTimeFromTuples(relTime)
        return
    # check for absolute dates/times of type 'tomorrow3am'
    dayMatches = re.match(dayRegex, timeString, re.VERBOSE)
    if dayMatches:
        # warning: also matches '' and impossible times
        print 'day: %s %s' % dayMatches.group('day', 'time')
        return
    print 'noMatch: ', timeString



dateStrings = ['march10', 'may31', 'feb28']
relativeStrings = ['1months2days', '4hours', '15year', '7h', '11MONTHS', '12dAyS']
dayStrings = ['monday', 'mon', 'mon9am', 'tomorrow9am', 'today9am', 'wed15h', 'THU', 'tOmOrrOw1am']
badStrings = ['months1', '7s', 'gibberish', '11slkfji', '', '9am', '13am', 'tomorrow25h', 'march', '12', 'february30']


print '\nTesting relative strings'
for s in relativeStrings:
    checkStringForTime(s)

print '\nTesting day strings'
for s in dayStrings:
    checkStringForTime(s)

print '\nTesting date strings'
for s in dateStrings:
    checkStringForTime(s)

print '\nTesting bad strings'
for s in badStrings:
    checkStringForTime(s)
