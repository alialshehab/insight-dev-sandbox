import logging
from pyspark import SparkContext, SparkConf
import pyspark_cassandra
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['54.175.157.12']) #seed node ip
session = cluster.connect()
KEYSPACE = "keyspace_batch"

log = logging.getLogger('b')

log.debug("creating keyspace...")

rows = session.execute("SELECT keyspace_name FROM system.schema_keyspaces")
if KEYSPACE in [row[0] for row in rows]:
    log.debug("There is an existing keyspace...")
    log.debug("setting keyspace...")
    session.set_keyspace(KEYSPACE)
else:
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
        """ % KEYSPACE)

    log.debug("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    log.debug("creating table...")
    session.execute("""
        CREATE TABLE mytable_rdd ( fake int, hour int, number_of_users int, PRIMARY KEY ((fake), hour))  with clustering ORDER BY (hour DESC) 
       """) 
#### Code starts Here ####
def mapper(line):
        gps_push = line.split(";")
        return ((gps_push[0],int(gps_push[1][0:8]+gps_push[1][9:11])),(gps_push[-2]=='True')*1)

conf = SparkConf().setAppName("myBatch")
sc = SparkContext(conf=conf)
data = sc.textFile("hdfs://ec2-52-2-54-47.compute-1.amazonaws.com:9000/data2/kafka_b*.dat")
formatted_data = data.map(lambda line: mapper(line)).distinct().map(lambda tuple:(tuple[0][1],tuple[1])).reduceByKey(lambda a,b: a+b).map(lambda a: (1,a[0],a[1]))
#tt = formatted_data.collect()
#for val in tt:
#	print val

#def parse_tuple(hour, count):
#    return (hour, count) # grab two arguments and return as a list

#mapped = formated_data.map(lambda line: parse_tuple(line[0], line[1])) # return a list
formatted_data.saveToCassandra("keyspace_batch", "mytable_rdd",)
