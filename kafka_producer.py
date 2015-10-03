# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:02:22 2015

@author: alialshehab
"""

import random
import sys
import six
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer
import time

class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)
        self.minLat = 40.708751 
        self.maxLat = 40.802895
        self.minLong = -74.025879
        self.maxLong = -73.930435
        self.counter_start = 0
        # self.locs = [(40.75280785, -73.97546422),(40.73988115,-73.98711691),(40.76105171, -73.96962834),\
        #                 (40.75790096,-73.97578395),(40.75833353,-74.00436092),(40.74496999,-73.97087089),\
        #                 (40.76088942,-73.97008963),(40.75494802,-73.96084512),(40.73754566,-73.98306014),\
        #                 (40.76804075,-73.98086881),(40.73795777,-73.97972054),(40.75311322,-73.99081106),\
        #                 (40.76445038,-73.9693873),(40.75204099,-73.99041951),(40.75705723,-73.98304045),\
        #                 (40.74984862,-73.98108846),(40.73641334,-73.99263483),(40.74022644,-73.97511118),\
        #                 (40.74081696,-73.99869147),(40.75155827,-73.97809876),(40.7979499,-73.93799602),\
        #                 (40.78487376,-73.9488285),(40.78891306,-73.96322338),(40.80932537,-73.95927604),\
        #                 (40.79512142,-73.97732225),(40.78566559,-73.94358666),(40.80024399,-73.96799964),\
        #                 (40.78788311,-73.97040765),(40.80434947,-73.93874699),(40.80183406,-73.96247845),\
        #                 (40.80595751,-73.95441724),(40.80650874,-73.96646741),(40.7931067,-73.9413598),\
        #                 (40.81627861,-73.95581725),(40.80999546,-73.96029616),(40.81289571,-73.95471676),\
        #                 (40.81689372,-73.93035378),(40.81309684,-73.92121306), (40.8096491,-73.93651239)]
        self.available=[[8,9,10, 17,18,19,20,21],[8,9,10,11,16,17,18,19,20],[8,9,15,16,17,18],\
                            [14,15,16,17,18,19,20,21,22],[10,11,12,22,23,00],[12,13,14,15,16],\
                            [19,20,21,22,23,00],[00,01,02],[8,11,13,15,17,19,21,22,23], [8,2],\
			    [0,1,2,3,4,5,6,7,8,9,10,12],[13,14,15,16,17,18,19,20,21,22,23]]

    def produce_msgs(self, name):
        # location_index = random.randint(0, len(self.locs))               
        # latitude = self.locs[location_index][0]
        # longitude = self.locs[location_index][1]
        lat_frac = random.random()
        long_frac = random.random()               
        latitude = lat_frac*self.minLat + (1-lat_frac)*self.maxLat
        longitude = long_frac*self.minLong + (1-long_frac)*self.maxLong
        schedule = self.available[random.randint(0,len(self.available)-1)]
        steps = self.counter_start
        while True:
            direction = random.randint(0,4)
            t = datetime.now().strftime("%Y%m%d %H%M%S")
            hr = datetime.now().hour
            if hr == 0:
                steps = self.counter_start
            availability = hr in schedule
            if direction == 0:
                steps +=1
                if latitude >= self.maxLat:
                    latitude = latitude - 0.00001124152
                else:
                    latitude = latitude + 0.00001124152
            elif direction == 1:
                steps +=1
                if longitude >= self.maxLong:
                    longitude = longitude - 0.00001124152
                else:
                    longitude = longitude + 0.00001124152
            elif direction == 2:
                steps +=1
                if latitude <= self.minLat:
                    latitude = latitude + 0.00001124152
                else:
                    latitude = latitude - 0.00001124152
            elif direction == 3:
                steps +=1
                if latitude <= self.minLong:
                    longitude = longitude + 0.00001124152
                else:
                    longitude = longitude - 0.00001124152
            else:
                pass
            
            str_fmt = "{};{};{};{};{};{}"
            message_info = str_fmt.format("user_"+str(name),
                                          t,
                                          latitude,
                                          longitude,
                                          availability,
                                          steps)
            print message_info
            self.producer.send_messages('b', name, message_info)
            time.sleep(0.1)

if __name__ == "__main__":
#    p = Producer()
#    p.produce_msgs("ali")
    args = sys.argv
    ip_addr = str(args[1]) #name node ip
    partition_key = str(args[2]) #session name for partision
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key) 
