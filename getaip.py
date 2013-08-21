import urllib2
import sys
import AD
import re
import urllib
import os

AIPBASEURL = "http://www.aip.net.nz/"
AIPURL = "http://www.aip.net.nz/NavWalk.aspx?section=CHARTS"
response = urllib2.urlopen(AIPURL)

IFR_Keywords = ['VOR', 'RNAV', 'Standard Route Clearances', 'SID', 'ILS', 'Visual Arrivals']
aerodromes=[]

def add_single_ad(line, aerodrome=None):
   """ Gets a line of scraped html and returns an AD object """
   if not aerodrome:
      m = re.search('href="pdf/(.*)&#xD(.*)>(.*)</a>(.*)\((.*)\)', line)
      aerodrome = AD(name = m.group(3), ICAO_code = m.group(5))
   else:
      m = re.search('href="pdf/(.*)&#xD(.*)>(.*)</a>', line)
   aerodrome.assets.append(ad_asset(name = m.group(3).strip().replace("&amp;", "&"), filename = m.group(1)))
   return aerodrome

def add_multiple_ad(line):
   """ gets a multiple pdf aerodrome """
   m=re.search('href="(.*)">(.*)</a>(.*)\((.*)\)', line)
   print "Creating aerodrome with name %s" % m.group(2).strip()
   aerodrome = AD(name=m.group(2).strip(), ICAO_code=m.group(4))
   # now we need to get the list of pdf's
   response = urllib2.urlopen(AIPBASEURL + m.group(1).replace("&amp;", "&"))
   print "Getting all assets for %s at %s" % (aerodrome.name, AIPBASEURL + m.group(1).replace("&amp;", "&"))
   for line in response:
      if 'pdf' in line:
         add_single_ad(line, aerodrome)
   return aerodrome

if response.code != 200:
   print "Error connecting to AIP site"
   sys.exit(0)

for line in response:
   if 'pdf' in line:
      aerodromes.append(add_single_ad(line.strip()))
   if 'section=CHARTS&amp' in line:
      aerodromes.append(add_multiple_ad(line.strip()))

# now we have a full list of aerodromes with all assets

#download
os.mkdir('aip')
for aerodrome in aerodromes:
   if len(aerodrome.assets) > 0:
      # download all the assets for that aerodrome
      # 
      os.mkdir('aip/' + aerodrome.name);
      for asset in aerodrome.assets:
         for word in IFR_Keywords:
            if word not in asset.name:
               print "Downloading %s for %s" % (asset.name, aerodrome.name)
               urllib.urlretreive(asset.url, 'aip/' + aerodrome.name + '/' + asset.name + '.pdf')
            else:
               print "NOT downloading IFR document %s for %s" % (asset.name, aerodrome.name)
