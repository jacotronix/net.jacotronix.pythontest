'''
Created on 18 Nov 2012

@author: Jamie
'''

#i2C BMP085 Pressure & Temperature Sensor Driver

#Code for this is mainly referenced from these 2 sources:

#Maarten Damen’s Bus Pirate reading the BMP085 Temperature
#http://www.maartendamen.com/2011/04/bus-pirate-reading-bmp085-temperature/

#Python port of John Burn’s C Code in Reading data from a Bosch BMP085 with a Raspberry Pi
#http://www.john.geek.nz/2012/08/reading-data-from-a-bosch-bmp085-with-a-raspberry-pi/

#!/usr/bin/env python

import smbus
import time

class BMP085():
    OSS = 3

    def __init__(self, i2c, address):
        self.i2c = i2c
        self.address = address
        self.ac1 = self.readSignedWord(0xaa)
        self.ac2 = self.readSignedWord(0xac)
        self.ac3 = self.readSignedWord(0xae)
        self.ac4 = self.readWord(0xb0)
        self.ac5 = self.readWord(0xb2)
        self.ac6 = self.readWord(0xb4)
        self.b1 = self.readSignedWord(0xb6)
        self.b2 = self.readSignedWord(0xb8)
        self.mb = self.readSignedWord(0xba)
        self.mc = self.readSignedWord(0xbc)
        self.md = self.readSignedWord(0xbe)

    def readWord(self, reg):
        msb = self.i2c.read_byte_data(self.address, reg)
        lsb = self.i2c.read_byte_data(self.address, reg+1)
        value = (msb << 8) + lsb
        return value

    def readSignedWord(self, reg):
        msb = self.i2c.read_byte_data(self.address, reg)
        lsb = self.i2c.read_byte_data(self.address, reg+1)
        if (msb > 127):
            msb = msb - 256
        value = (msb << 8) + lsb
        return value

    def readUT(self):
        self.i2c.write_byte_data(self.address, 0xf4, 0x2e)
        time.sleep(0.0045)
        ut = self.readWord(0xf6)
        return ut

    def readTemperature(self):
        ut = self.readUT()
        x1 = ((ut - self.ac6) * self.ac5) >> 15
        x2 = (self.mc << 11) / (x1 + self.md)
        self.b5 = x1 + x2
        return ((self.b5 + 8) >> 4) / 10.0

    def readUP(self):
        self.i2c.write_byte_data(self.address, 0xf4, 0x34 + (self.OSS << 6))
        delay = (2 + (3 << self.OSS)) / 1000.0
        time.sleep(delay)
        msb = self.i2c.read_byte_data(self.address, 0xf6)
        lsb = self.i2c.read_byte_data(self.address, 0xf7)
        xlsb = self.i2c.read_byte_data(self.address, 0xf8)
        up = (msb << 16) + (lsb << 8) + xlsb
        up = up >> (8 - self.OSS)
        return up

    def readPressure(self):
        up = self.readUP()
    
        b6 = self.b5 - 4000
    
        x1 = (self.b2 * (b6 * b6)>>12)>>11
        x2 = (self.ac2 * b6)>>11
        x3 = x1 + x2
        b3 = (((self.ac1 * 4 + x3)<<self.OSS) + 2)>>2
    
        x1 = (self.ac3 * b6)>>13
        x2 = (self.b1 * ((b6 * b6)>>12))>>16
        x3 = ((x1 + x2) + 2)>>2
        b4 = (self.ac4 * (x3 + 32768))>>15
    
        b7 = (up - b3) * (50000>>self.OSS)
    
        if (b7 < 0x80000000):
            p = (b7<<1)/b4
        else:
            p = (b7/b4)<<1
    
        x1 = (p>>8) * (p>>8)
        x1 = (x1 * 3038)>>16
        x2 = (-7357 * p)>>16
        p += (x1 + x2 + 3791)>>4
    
        return p

if __name__ == "__main__":
    
    i2c = smbus.SMBus(0)
    bmp085 = BMP085(i2c, 0x77)
    t = bmp085.readTemperature()
    p = bmp085.readPressure()
        
    print "Temperature: %.2f C" % t
    print "Pressure:    %.2f hPa" % (p / 100)
