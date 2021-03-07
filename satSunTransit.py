import math

def degToRad(deg, mins=0, sec=0):
    mins += sec/60.0
    deg += mins/60.0
    rad = deg * math.pi/180.0
    return rad

def radToDeg(rad):
    deg = rad * 180.0/math.pi
    return deg

def radToDegMinSec(rad):
    if rad < 0:
        rad += math.pi * 2
    deg = radToDeg(rad)
    arcmin = (deg - math.floor(deg))*60
    arcsec = (arcmin - math.floor(arcmin)) * 60
    
    deg = math.floor(deg)
    arcmin = math.floor(arcmin)
    return deg, arcmin, arcsec

def radToTimeAngle(rad):
    if rad < 0:
        rad += math.pi * 2
    h = rad * 12 / math.pi
    m = (h - math.floor(h))*60
    s = (m - math.floor(m))*60
    h = math.floor(h)
    m = math.floor(s)
    
    return h, m, s
    

REarth = 6370.0
RSat = 42164.0
satLong = degToRad(13.0)
spring = 20.44236
tilt = degToRad(23.439)
year = 365.256

def satPosition(latitude, longitude):
    deltaLong = longitude - satLong
    ortodrome = math.acos(math.cos(latitude) * math.cos(deltaLong))
    azimuth = math.asin(math.sin(deltaLong)/math.sin(ortodrome)) + math.pi
    dist = math.sqrt(REarth**2 + RSat**2 - 2 * REarth * RSat * math.cos(ortodrome))
    height = math.acos((RSat**2 - REarth**2 - dist**2)/(-2 * REarth * dist)) - math.pi/2
    return azimuth, height


def azHeightToTimeDec(azimuth, height, latitude):
    dec = math.pi/2 - math.acos(math.cos(azimuth) * math.cos(height) * math.cos(latitude) + math.sin(height) * math.sin(latitude))
    timeAngle = math.asin(math.sin(math.pi * 2 - azimuth) * math.cos(height) / math.cos(dec))
    return dec, timeAngle

def sunEclLong(sunDec):
    return math.asin(math.sin(sunDec)/math.sin(tilt))

def main():
    latitude = degToRad(52, 13, 47)
    longitude = degToRad(21, 0, 42)
    az, h = satPosition(latitude, longitude)
    dec, t = azHeightToTimeDec(az, h, latitude)
    sunEcl = sunEclLong(dec)
    date = sunEcl * year / (2*math.pi)*0.9935 + spring
    print("March", math.floor(date))
    h, m, s = radToTimeAngle(t + math.pi)
    print(h, ":", m, ":", round(s))
    
main()
