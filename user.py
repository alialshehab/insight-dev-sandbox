# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 22:15:00 2015

@author: alialshehab
"""
import random
import json

class User():
    
    def __init__(self, name, available = True):
        self.minLat = 40.708751 
        self.maxLat = 40.802895
        self.minLong = -74.025879
        self.maxLong = -73.930435
        self.name = name
        self.time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        frac = random.random()
        self.latitude = frac*self.minLat + (1-frac)*self.maxLat
        self.longitude = frac*self.minLong + (1-frac)*self.maxLong
  
#        self.latitude = latitude
#        self.longitude = longitude
        self.available = available
        #For the city of manhattan        
        
        
    def random_walk(self):
        '''
        Generate a days trajectory
        '''
        f = open(self.name + ".txt", 'w')
        for i in range(86400/12): #86400 seconds in a day
            # one unit of time is 12 seconds
            self.time = self.time+1
            direction = random.randint(0,2)
            # normally humans walks 0.00013489824/12 latitude variance per 12 secs
            # citation: Human Centric Technology and Service in Smart Space: HumanCom 2012                       
            if direction == 0:
                self.latitude = self.latitude + 0.00013489824
            else if:
                self.longitude = self.longitude + 0.00013489824
                
            json.dump({self.name:[self.time, self.longitude, self.latitude]}, f)
            f.write('\n')
        f.close()
    
    
    def get_latitude(self):
        return self.latitude
        
    def get_longitude(self):
        return self.longitude
        
if __name__ == "__main__":
    for i in range(5):
        u = User("user_"+ str(i))
        u.random_walk()