import urllib2
import sys
import AD
import re

AIPURL = "http://www.aip.net.nz/NavWalk.aspx?section=CHARTS"
response = urllib2.urlopen(AIPURL)

aerodromes=[]

if response.code != 200:
   print "Error connecting to AIP site"
   sys.exit(0)

raw_ad_single_pdf = []
raw_ad_multiple_pdf = []

for line in response:
   if 'pdf' in line:
      aerodromes.append(add_single_ad(line.strip()))

   if 'section=CHARTS&amp' in line:
      aerodromes.append(add_multiple_ad(line.strip()))



   
