# AIP Aerodrome class
import re
import urllib2

AIPBASEURL = "http://www.aip.net.nz/"

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

class AD:
   def __init__(self, name, ICAO_code):
      self.name = name
      self.ICAO_code = ICAO_code
      self.assets = []

class ad_asset:
   def __init__(self, name, filename, url = None, md5 = None):
      self.name = name
      self.filename = filename
      if url is None:
         self.url = AIPBASEURL + "pdf/" + filename
      self.md5 = md5
