import urllib2, cookielib
import sys
from AD import *
import re
import urllib
import os
import shutil

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
response = opener.open('http://www.aip.net.nz/Default.aspx')
# get __VIEWSTATE and __EVENTVALIDATION values to submit to form
for line in response:
   if '__VIEWSTATE' in line:
      m = re.search('value="(.*)"(.*)', line)
      viewstate = m.group(1)
   elif '__EVENTVALIDATION' in line:
      m = re.search('value="(.*)"(.*)', line)
      eventvalidation = m.group(1)

login_data = urllib.urlencode({'btnAgree': '  I Agree  ', '__VIEWSTATE': viewstate, '__EVENTVALIDATION': eventvalidation})
opener.open('http://www.aip.net.nz/Default.aspx', login_data)

AIPBASEURL = "http://www.aip.net.nz/"
AIPURL = "http://www.aip.net.nz/NavWalk.aspx?section=CHARTS"
#response = urllib2.urlopen(AIPURL)
response = opener.open(AIPURL)

IFR_Keywords = ['VOR', 'RNAV', 'Standard Route Clearances', 'SID', 'ILS', 'Visual Arrivals', 'NDB', 'DME']
aerodromes=[]

if response.code != 200:
   print "Error connecting to AIP site"
   sys.exit(0)


print "Successfully connected to AIP site"

for line in response:
   if 'pdf' in line:
      aerodromes.append(add_single_ad(line.strip()))
   if 'section=CHARTS&amp' in line:
      aerodromes.append(add_multiple_ad(line.strip()))

# now we have a full list of aerodromes with all assets

#download
#if os.path.exists('aip'):
#  shutil.rmtree('aip')
if not os.path.exists('aip'):
   os.mkdir('aip')
for aerodrome in aerodromes:
   if len(aerodrome.assets) > 0:
      # download all the assets for that aerodrome
      if not os.path.exists(os.path.normcase('aip/' + re.escape(aerodrome.ICAO_code))):
         os.mkdir(os.path.normcase('aip/' + aerodrome.ICAO_code));
      print "Downloading all assets for %s" % aerodrome.name
      for asset in aerodrome.assets:
         if not any(word.lower() in asset.name.lower() for word in IFR_Keywords):
            #response = urllib2.urlopen(asset.url)
            response = opener.open(asset.url)
            if response.code == 200:
               fh = open(os.path.normcase('aip/' +  aerodrome.ICAO_code + '/' + asset.name + '.pdf'), "w")
               fh.write(response.read())
               fh.close()
            else:
               print "Error downloading file %s" % asset.url


print """ To sync with Air Nav Pro, start web dav server on Air Nav Pro, mount web dav share
and run:

rsync -av --checksum --delete aip/ /Volumes/{WEBDAVMOUNT}/Documents/Airport\ charts/

where {WEBDAVMOUNT} is the address of the webdav server (air nav pro)

You will need to reindex document in Air Nav Pro, to update the changes
"""

