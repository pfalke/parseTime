"""
Convert a string to a python datetime.

Below are sample inputs that should work once everyting is done.

- absolute dates
wednesday
wed
may10
tomorrow

- absolute datetimes
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

relativeRegex = re.compile('(\d+)(year|y|month|m|week|w|day|d|hour|h|minute|min)s?')

# return test from test@example.com
def getEmailRecipient(emailAdress):
	matchObj = re.match(r'(\w+)@', emailAdress)
	if matchObj:
		return matchObj.group(1)
	return None

def relativeTime(timeString):
	matches = relativeRegex.findall(timeString)
	print matches




GoodStrings = ['11months23days', '4hours', '15year', '7h']
BadStrings = ['months1', '7s', 'gibberish', '11slkfji']


print '\nTesting good strings'
for s in GoodStrings:
	relativeTime(s)

print '\nTesting bad strings'
for s in BadStrings:
	relativeTime(s)
