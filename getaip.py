import urllib2
import sys
from AD import *
import re
import urllib
import os
import shutil

AIPBASEURL = "http://www.aip.net.nz/"
AIPURL = "http://www.aip.net.nz/NavWalk.aspx?section=CHARTS"
response = urllib2.urlopen(AIPURL)

IFR_Keywords = ['VOR', 'RNAV', 'Standard Route Clearances', 'SID', 'ILS', 'Visual Arrivals']
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
shutil.rmtree('aip')
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
            response = urllib2.urlopen(asset.url)
            if response.code == 200:
               fh = open(os.path.normcase('aip/' +  aerodrome.ICAO_code + '/' + asset.name + '.pdf'), "w")
               fh.write(response.read())
               fh.close()
            else:
               print "Error downloading file %s" % asset.url
