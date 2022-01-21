import json, random, time, boto3, sys, glob, io, datetime
#import avro.schema, avro.io, avro.datafile,
from avro.io import DatumWriter
from kafka import KafkaConsumer
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

###########################################################################################
#                               DONT TOUCH
input_topic = sys.argv[1:][0]
if len(sys.argv[1:])==1:
    output_topic = input_topic
else:
    output_topic = sys.argv[1:][1]
    
SCHEMA_PATH =glob.glob("./*avsc")[0]

print("Reading data from {}, exporting calculations to {}.".format(input_topic, output_topic))

#   CONSUMER (import)
consumer = KafkaConsumer(input_topic,
                        group_id=None,
                        bootstrap_servers=['ec2-18-205-2-251.compute-1.amazonaws.com:9092'],
                        auto_offset_reset='earliest')

#   CALCULATION
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

# PRODUCER (export)
AvroProducerConf = {
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081',
    'broker.address.family': 'v4'
}

value_schema = avro.load(SCHEMA_PATH)
avroProducer = AvroProducer(
                   AvroProducerConf, 
                   default_value_schema=value_schema
               )

# Misc (keeping track of events)
count = 0
i=0
n=0
###########################################################################################

try:
    for msg in consumer:
        val = json.loads(msg.value.decode("utf-8"))
        
        # We'll only look at people who have geospacial coordinates for presentation purposes.
        if val['geo'] == None:
            if count%10 == 0:
                print("Counted {} without geographical coordinates.".format(count))
            count += 1
        else:
            print("Found somebody with Geo Cords:")

            res = json.dumps(comprehend.detect_sentiment(Text=val['text'], LanguageCode=val['lang']))
            res = json.loads(res)
            print('----')
            i+=1

            #######################
            # Clean up!
            
            # Dealing with missing data for location; let's dump it somewhere exotic
            # This shouldn't even matter; we're filtering out non-localizable cases.
            place = val['place']
            if place == None:
                geo = "MD"
            else:
                geo = place['country_code']

            if val['coordinates'] == None:
                cords = "18.7669,46.8691"
            else:
                print(val['coordinates'])
                cords=str(round(val['coordinates']['coordinates'][1],4)) +","+str(round(val['coordinates']['coordinates'][0],4))

            # Not going to report neutral score - it's boring. Not sure what to do with it.
            # Let's do our own elaborate calculation for demostration purposes.
            unrounded=(res['SentimentScore']['Positive']-res['SentimentScore']['Negative'])*100
            comp_score = round(unrounded,2)
            print("Composite score: {}".format(comp_score))
            
            # Convert milliseconds to datetime
            us = int(val['timestamp_ms'])
            ms = us/1000
            dt = datetime.datetime.fromtimestamp(ms).strftime("%Y-%m-%dT%H:%M:%S.%fZ")#('%c')
            print(dt)

            ########################
            # Pass through avro/Kafka

            value = {
                "company":input_topic,
                "user": val['user']['screen_name'],
                "tweet":val['text'],
                "timestamp":str(dt),
                "sentiment":res['Sentiment'],
                "compositeScore":comp_score,
                "negScore":round(res['SentimentScore']['Negative'],4),
                "posScore":round(res['SentimentScore']['Positive'],4),
                "geo":geo,
                "coordinates":cords
            }
            print(value)
            avroProducer.produce(topic=output_topic, value=value)
            avroProducer.flush()
            
            # Keeping track of neutral rate:
            if res['Sentiment']=="NEUTRAL":
                n+=1
            print("Neutral rate: {}%".format(n/(i+1)*100))    
            print("-------\n")
        
except KeyboardInterrupt:
    sys.stderr.write('%% Aborted by user\n')
    
'''



# This is for reading raw avro files from kafka. Terrible 
        bytes_reader = io.BytesIO(msg.value)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.datafile.DataFileReader(bytes_reader, avro.io.DatumReader())
        for thing in reader:
            try:
                if thing['retweeted']==False:
                    print("---")
                    print("User: {}, friends: {}, followers: {}.".format(thing['user_name'], 
                                                                         thing['user_friends_count'], 
                                                                         thing['user_followers_count']))
                    print("Text: {}".format(thing['text']))
                    print("Created at: {}.".format(thing['created_at']))
                    print("Replies: {}.".format(thing['retweet_count']))
                    #dump = json.dumps(thing)
                    #load = json.loads(dump)
                    #print(type(load))
                    sys.stdout.flush()
            except AssertionError:
                continue
'''
