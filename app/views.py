# -*- Encoding:utf-8 -*-
#  Created by Mads Ynddal on 31/08/15.
#  GitHub: https://github.com/Baekalfen/iCalFilter.git
#  License: Public Domain
#

from app import app
from flask import request
import urllib2
import re

whitelist = ['sjt402', 'qwv828']

CACHE = True

if CACHE:
    cacheMap = dict.fromkeys(whitelist)


def getCalendar(user):
    handle = urllib2.urlopen('https://personligtskema.ku.dk/ical.asp?objectclass=student&id=%s' % user)
    data = handle.read(1024**2)  # Max 1MB

    if len(data) < 20*1024:  # 20 KB (Tested data was >75 KB for success and <9 KB for errors)
        print "Data from server too small - probably an error. A cache will be used instead."
        cached = cacheMap.get(user)
        return "No cache available" if cached is None else cached
    else:
        #print "Request successfull"
        cacheMap[user] = data
        return data


@app.route('/getiCal', methods=['GET'])
def getiCal():
    KUName = request.args.get('kuname', '')
    print "Got name:", KUName
    if not KUName in whitelist:
        print "Rejected"
        return ""

    data = getCalendar(KUName)

    data, count = re.subn("SUMMARY:\d{4}-[A-Z]\d-\d[A-Z]\d{2};", "SUMMARY:", data)
    data, count = re.subn(" - Føv", " - Øvelser", data)
    print "Replaced:", count
    return data
