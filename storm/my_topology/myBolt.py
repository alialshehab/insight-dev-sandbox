import logging
from pyleus.storm import SimpleBolt

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import named_tuple_factory

cluster = Cluster(['54.175.157.12']) #seed node ip
session = cluster.connect()
KEYSPACE = "keyspace_realtime"

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
        CREATE TABLE mytable (
            name text,
            latitude float,
            longitude float,
            steps int,
	    status text,
            PRIMARY KEY (name)
        )
        """)

#query = SimpleStatement("""
#   INSERT INTO mytable (name, latitude, longitude)
#    VALUES (%(key)s, %(a)s, %(b)s)
#    """, consistency_level=ConsistencyLevel.ONE)
#prepared = session.prepare("""
#    INSERT INTO mytable (name, latitude, longitude)
#    VALUES (?, ?, ?)
#    """)

class myBolt(SimpleBolt):

    OUTPUT_FIELDS = ['data']

    def initialize(self):
#        self.unoccCabs = {}
        self.i = 0

    def process_tuple(self, tup):
        result, = tup.values
        #cabID, lat, lng, occ, timestamp = result.split(",")
        for k, value in result.items():
            data = value
        name, timestamp, latitude, longitude, availability, steps = data.split(";")

        #if (occ != '\N'):  # check to ensure that there are no null values
        #    if int(occ) == 0:
        #        self.unoccCabs[cabID] = {'c:lat': lat, 'c:lng': lng}  # add unoccupied cab to table
        #    else:
        #        if int(occ) == 1:
        #            if (cabID in self.unoccCabs.keys()):
        #                del self.unoccCabs[cabID]
        #                #minuteTbl.delete('StormData', columns=['c:' + cabID]) # remove cab from table if it is now occupied
#        if availability == True:
        log.debug(name + "," + timestamp + "," + latitude + "," + longitude + "," + availability + ","+steps + ", inserting %d into cassandra..." % self.i)
#        session.execute(query, dict(key=name, a=latitude, b=longitude))
	session.execute("""INSERT INTO mytable (name, latitude, longitude, status, steps) VALUES (%s, %s, %s, %s, %s)""", (name, float(latitude), float(longitude), availability, int(steps)))
	self.i +=1

    #def process_tick(self):
    #    cur_cabs = self.unoccCabs
    #    colDict = {}
    #    for key, val in cur_cabs.iteritems():
    #        colDict['c:' + key] = json.dumps(val) # Add currently available cabs to HBase
    #    #minuteTbl.put('StormData', colDict)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/b.log',
        filemode='a',
    )

    myBolt().run()
