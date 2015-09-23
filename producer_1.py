# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 22:03:47 2015

@author: alialshehab
"""

import os
import sys
from kafka import KafkaClient, KeyedProducer, SimpleConsumer
from datetime import datetime
import time
import json

kafka = KafkaClient("54.175.48.121:9092")
source_file = '/Users/alialshehab/Desktop/InsightDataEngineering/InsightProject/user_0.txt'

def genData(topic):
    producer = KeyedProducer(kafka)
    while True:
        ifile = open(source_file)
        for line in ifile:
            key = line[7]
            producer.send(topic, key, line)
            time.sleep(0.1)  # Creating some delay to allow proper rendering
        ifile.close()

genData("sentences")