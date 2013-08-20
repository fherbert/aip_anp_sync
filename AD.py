# AIP Aerodrome class

class AD:
   def __init__(self, name, ICAO_code):
      self.name = name
      self.ICAO_code = ICAO_code
      self.assets = []

class ad_asset:
   def __init__(self, name, filename, url, md5 = None):
      self.name = name
      self.filename = filename
      self.url = url
      self.md5 = md5

