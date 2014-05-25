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
    (?P<day>monday|mon|tuesday|tue|wednesday|wed|thursday|thu|friday|fri|saturday|sat|sunday|sun|tomorrow|)     # either weekday or tomorrow, optional
    (?P<time>\d{1,2}(?:am|pm|h)|)                                                                               # 9pm same as 21h, optional
    $
    '''

# return test from test@example.com, does not check if the string is a valid email address
def getEmailRecipient(emailAdress):
    matchObj = re.match(r'([a-z0-9\.]+)@', emailAdress)
    if matchObj:
        return matchObj.group(1)
    return None

def relativeTimeInString(timeString):
    # recursively extract relative time data from string, returns list of tuples like [(2, 'months')]
    relMatches = re.match(relativeRegex, timeString, re.VERBOSE)
    if relMatches:
        return [relMatches.group('number', 'type')] + relativeTimeInString(relMatches.group('remainingString'))
    return []

def checkStringForTime(timeString):
    # convert to lowercase
    timeString = timeString.lower()
    relTime = relativeTimeInString(timeString)
    if relTime:
        print 'relative: ', relTime
        return
    dayMatches = re.match(dayRegex, timeString, re.VERBOSE)
    if dayMatches:
        # also matches '' and impossible times
        print 'day: ', dayMatches.group()
        return
    print 'noMatch: ', timeString




relativeStrings = ['11months23days', '4hours', '15year', '7h', '11MONTHS', '12dAyS']
dayStrings = ['monday', 'mon', 'mon9am', 'tomorrow9am', '9am', 'wed15h', 'THU', 'tOmOrrOw1am']
badStrings = ['months1', '7s', 'gibberish', '11slkfji', '', '13am', 'tomorrow25h']


print '\nTesting relative strings'
for s in relativeStrings:
    checkStringForTime(s)

print '\nTesting day strings'
for s in dayStrings:
    checkStringForTime(s)

print '\nTesting bad strings'
for s in badStrings:
    checkStringForTime(s)
