# LetsHang [Insight Data Engineering]
======================================

## An application to help friends hangout and encourage excercise
[www.letshang.xyz](http://52.2.54.47:5000/)

##Table of Contents

1. Introduction
2. Data sources
3. Pipeline
  - Ingestion
  - File Distribution
  - Realtime Streaming
  - Batch Processing
  - Database
  - Front End
4. Cluster Setup
5. Dependencies
6. Future Work
7. Acknowledgements

#1. Introduction

LetsHang is an application that uses users geolocation data and availability status to help friends hangout and encourage each other to excercise "walk" more. The app provides a map with users realtime location, availability status and the total number of steps walked by the user in a given day. It also provides a graph showing the number of users available at different hours of the day.

![Realtime Demo] (images/map.png)
![Batch Demo] (images/graph.png)

#2. Data Sources

Data sources for this application are user's (friends) the gps location and availability status. The gps location is provided by the users mobile device and the availability status is provided manually by the user or through the users calender.

To test the application, a python program was used to produce a real time streams of geolocation data of users walking around NYC. The availability status was generated by a python program that reads in some predefined google calender schedules. The application was tested using 5000 producers simultaniously sending messages every 0.1 secnds. A message constituted of "user_name, time_stamp, user_latitude, user_longitude, user_availability." For exmple: "user_20, 20151002 185127, 40.7643503305, -73.9694356385, False"

#3. Pipeline

![pipeline Demo] (images/pipeline.png)


* Ingestion: The producers published the data to Apache Kafaka with 4 brokers which were setup on a cluster of 4 nodes. The data was split into 4 partitions with a replication factor of 2. Data was then consumed by camus (ingestion framework) that pushed the information to HDFS for batch processing and a Apache Storm for realtime streaming and processing. Ingestion was coordinated using Zookeeper and monitored using Kafka Manager. The measured throughput was 10GB/hr.

* File Distribution: HDFS provides distributed storage throughout the cluster. To play to HDFS's strength of easily storing few large files over smaller ones, files were stored in 128 MB blocks out of 128 MB.

* Realtime Streaming: Realtime streaming and processing was implemented using Apache Storm. Storm nimbus and supervisors were setup on 4 nodes.The storm topolgy used had a single Kafka Spout and two processing Bolts. The Bolts pushed the data to a Cassandra data base. The measured latency of the slower path was 30ms. The nature of the application warranted using Storm instead of Spark streaming.
	
* Batch Processing: Spark was used to process the information stored on HDFS. MapReduce functions were used to transform the data before pushing it to a Cassandra database.
	
* Database: Cassandra was used with two tables. The aim was to have the realtime information immediately available able to be queried from the API apart from the batch processing table which gets updated less frequently by a cron every hour. Cassandra presented itself as the ideal database for the purposes since the application presents time series data and availablility is important for social applications.
	
* Front-End Application: I used Flask for website handling, with Bootstrap for the template, as well as Google Maps and Hichart for displaying user locations and batch jobs.

#4. Cluster Setup

![Cluster Setup] (images/cluster.png)

#5. Dependencies

I used the following open-source packages for connectors between the technologies outlined above:
* CqlEngine for Pyspark and Cassandra.
* Pyleus and cassandra driver for Kafka-Storm-Cassandra.

#6. Future Work
	
I would like to implemnt a reactive feature that notifies users when they are closer to each other and free. Elastic search could be used to achieve this functionality.

#7. Acknowledgements

Many thanks to the Insight team for the wonderful opportunity and my fellow Fellows for their support.
