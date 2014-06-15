#!/usr/bin/python

#
# Copied directly from http://michelanders.blogspot.ru/2010/12/calulating-sunrise-and-sunset-in-python.html
#
# Anthony Toole, 2014: modified to return datetime.datetime (rather than
# datetime.time) if requested.  This makes more sense (as naturally every time
# is referring to a specific date, because it has to be specified to calculate
# the sunrise) and means that differences can be calculated on the returned
# values.

from math import cos,sin,acos,asin,tan
from math import degrees as deg, radians as rad
from datetime import date,datetime,time,timedelta

# this module is not provided here. See text.
from timezone import LocalTimezone

class sun:
 """ 
 Calculate sunrise and sunset based on equations from NOAA
 http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html

 typical use, calculating the sunrise at the present day:
 
 import datetime
 import sunrise
 s = sun(lat=49,long=3)
 print('sunrise at ',s.sunrise(when=datetime.datetime.now())
 """
 def __init__(self,lat=52.37,long=4.90, return_dates=False):
  """Initialise sun object for the specified location, defaulting to Amsterdam

  lat and long arguments must be in decimal (rather than degrees, minutes,
  seconds format)

  If return_dates is False (default) then datetime.time objects will be
  returned.  If True then datetime.datetime objects will be created - which
  have the benefit of encoding the day that the calculation was done for, as
  well as making it possible to calculate differences (eg. between sunrise and
  current datetime).
  """
  self.lat=lat
  self.long=long
  self.return_dates = return_dates
  
 def sunrise(self, when=None, tomorrow=False):
  """
  return the time of sunrise as a datetime.time object or datetime.datetime
  object (depending on value of self.return_dates)
  when is a datetime.datetime object. If none is given
  a local time zone is assumed (including daylight saving
  if present)
  tomorrow flag will be used if when is not specified to
  add one complete day to current datetime
  """
  if when is None:
    when = datetime.now(tz=LocalTimezone())
    if tomorrow:
      when += timedelta(days=1)
  self.__preptime(when)
  self.__calc()
  sunrise = sun.__timefromdecimalday(self.sunrise_t)
  if self.return_dates:
    sunrise = datetime.combine(when, sunrise)
  return sunrise

  
 def sunset(self, when=None, tomorrow=False):
  if when is None:
    when = datetime.now(tz=LocalTimezone())
    if tomorrow:
      when += timedelta(days=1)
  self.__preptime(when)
  self.__calc()
  sunset = sun.__timefromdecimalday(self.sunset_t)
  if self.return_dates:
    sunset = datetime.combine(when, sunset)
  return sunset
  
 def solarnoon(self, when=None, tomorrow=False):
  if when is None:
    when = datetime.now(tz=LocalTimezone())
    if tomorrow:
      when += timedelta(days=1)
  self.__preptime(when)
  self.__calc()
  solarnoon = sun.__timefromdecimalday(self.solarnoon_t)
  if self.return_dates:
    solarnoon = datetime.combine(when, solarnoon)
  return solarnoon
  
 @staticmethod
 def __timefromdecimalday(day):
  """
  returns a datetime.time object.
  
  day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5
  """
  hours  = 24.0*day
  h      = int(hours)
  minutes= (hours-h)*60
  m      = int(minutes)
  seconds= (minutes-m)*60
  s      = int(seconds)
  return time(hour=h,minute=m,second=s)

 def __preptime(self,when):
  """
  Extract information in a suitable format from when, 
  a datetime.datetime object.
  """
  # datetime days are numbered in the Gregorian calendar
  # while the calculations from NOAA are distibuted as
  # OpenOffice spreadsheets with days numbered from
  # 1/1/1900. The difference are those numbers taken for 
  # 18/12/2010
  self.day = when.toordinal()-(734124-40529)
  t=when.time()
  self.time= (t.hour + t.minute/60.0 + t.second/3600.0)/24.0
  
  self.timezone=0
  offset=when.utcoffset()
  if not offset is None:
   self.timezone=offset.seconds/3600.0
  
 def __calc(self):
  """
  Perform the actual calculations for sunrise, sunset and
  a number of related quantities.
  
  The results are stored in the instance variables
  sunrise_t, sunset_t and solarnoon_t
  """
  timezone = self.timezone # in hours, east is positive
  longitude= self.long     # in decimal degrees, east is positive
  latitude = self.lat      # in decimal degrees, north is positive

  time  = self.time # percentage past midnight, i.e. noon  is 0.5
  day      = self.day     # daynumber 1=1/1/1900
 
  Jday     =day+2415018.5+time-timezone/24 # Julian day
  Jcent    =(Jday-2451545)/36525    # Julian century

  Manom    = 357.52911+Jcent*(35999.05029-0.0001537*Jcent)
  Mlong    = 280.46646+Jcent*(36000.76983+Jcent*0.0003032)%360
  Eccent   = 0.016708634-Jcent*(0.000042037+0.0001537*Jcent)
  Mobliq   = 23+(26+((21.448-Jcent*(46.815+Jcent*(0.00059-Jcent*0.001813))))/60)/60
  obliq    = Mobliq+0.00256*cos(rad(125.04-1934.136*Jcent))
  vary     = tan(rad(obliq/2))*tan(rad(obliq/2))
  Seqcent  = sin(rad(Manom))*(1.914602-Jcent*(0.004817+0.000014*Jcent))+sin(rad(2*Manom))*(0.019993-0.000101*Jcent)+sin(rad(3*Manom))*0.000289
  Struelong= Mlong+Seqcent
  Sapplong = Struelong-0.00569-0.00478*sin(rad(125.04-1934.136*Jcent))
  declination = deg(asin(sin(rad(obliq))*sin(rad(Sapplong))))
  
  eqtime   = 4*deg(vary*sin(2*rad(Mlong))-2*Eccent*sin(rad(Manom))+4*Eccent*vary*sin(rad(Manom))*cos(2*rad(Mlong))-0.5*vary*vary*sin(4*rad(Mlong))-1.25*Eccent*Eccent*sin(2*rad(Manom)))

  hourangle= deg(acos(cos(rad(90.833))/(cos(rad(latitude))*cos(rad(declination)))-tan(rad(latitude))*tan(rad(declination))))

  self.solarnoon_t=(720-4*longitude-eqtime+timezone*60)/1440
  self.sunrise_t  =self.solarnoon_t-hourangle*4/1440
  self.sunset_t   =self.solarnoon_t+hourangle*4/1440

if __name__ == "__main__":
 s=sun(lat=52.37,long=4.90)
 print(datetime.today())
 print(s.sunrise(),s.solarnoon(),s.sunset())
