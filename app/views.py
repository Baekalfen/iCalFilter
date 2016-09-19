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


@app.route('/getiCal', methods=['GET'])
def getiCal():
    KUName = request.args.get('kuname', '')
    print "Got name:", KUName
    if not KUName in whitelist:
        print "Rejected"
        return ""
    handle = urllib2.urlopen(
        'https://personligtskema.ku.dk/ical.asp?objectclass=student&id=%s' % KUName)
    data = handle.read(1024**2)  # Max 1MB
    data, count = re.subn("SUMMARY:\d{4}-[A-Z]\d-\d[A-Z]\d{2};", "SUMMARY:", data)
    data, count = re.subn(" - Føv", " - Øvelser", data)
    print "Replaced:", count
    return data
