# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:29:32 2015

@author: alialshehab
"""

# Kafka producer that reads the input data in a loop in order to simulate real time events
import os
import sys
from kafka import KafkaClient, KeyedProducer, SimpleConsumer
from datetime import datetime
import time
import json

kafka = KafkaClient("54.175.48.121:9092")

source_file = '/Users/alialshehab/Desktop/InsightDataEngineering/InsightProject/user_2.txt'

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
