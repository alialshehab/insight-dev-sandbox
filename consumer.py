import time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
import os

class Consumer(object):
    def __init__(self, addr, group, topic):
        self.client = KafkaClient(addr)
        self.consumer = SimpleConsumer(self.client, group, topic,
                                       max_buffer_size=1310720000)
        self.temp_file_path = None
        self.temp_file = None
        self.topic = topic
        self.group = group
        self.block_cnt = 0

        os.system ( "hdfs dfs -mkdir /data2" )

    def consume_topic(self, output_dir):
        if not os.path.isdir ( output_dir ): os.makedirs ( output_dir )

        timestamp = time.strftime('%Y%m%d%H%M%S')

        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,
                                                         self.topic,
                                                         self.group,
                                                         timestamp)
        self.temp_file = open(self.temp_file_path,"w")

        while True:
            try:
                # get 1000 messages at a time, non blocking
                messages = self.consumer.get_messages(count=1000, block=False)

                # OffsetAndMessage(offset=43, message=Message(magic=0,
                # attributes=0, key=None, value='some message'))
                for message in messages:
                    self.temp_file.write(message.message.value + "\n")

                # file size > 40MB
                if self.temp_file.tell() > 40000000:
                    self.flush_to_hdfs(output_dir)

                self.consumer.commit()
            except:
                # move to tail of kafka topic if consumer is referencing
                # unknown offset
                self.consumer.seek(0, 2)


    def flush_to_hdfs(self, output_dir):

        self.temp_file.close()

        timestamp = time.strftime('%Y%m%d%H%M%S')

        print "Block {}: Flushing 40MB file to HDFS => /data2".format(str(self.block_cnt))
        self.block_cnt += 1

        # place blocked messages into history and cached folders on hdfs
        os.system("hdfs dfs -copyFromLocal %s %s" % (self.temp_file_path,
                                                        "/data2"))
        os.remove(self.temp_file_path)

        timestamp = time.strftime('%Y%m%d%H%M%S')

        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,
                                                         self.topic,
                                                         self.group,
                                                         timestamp)
        self.temp_file = open(self.temp_file_path, "w")


if __name__ == '__main__':
    print "\nConsuming messages..."
    cons = Consumer(addr="52.2.54.47:9092", group="hdfs", topic="b")
    cons.consume_topic("/tmp/tempfile")
