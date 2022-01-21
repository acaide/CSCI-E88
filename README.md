# CSCI-E88
Principles of Big Data Processing, Fall 2018


## Final Project

Inspired by my job at the time (2018), I built an end-to-end streaming NLP pipeline. Data was collected from Twitter via Flume, with help of the Twitter API. Tweaking the Flume source files was required to extract non-standard parameters from twitter, such as geo-spacial coordinates and user information. The text data will be analyzed with AWS Comprehend to obtain sentiment scores, but only if geo-spacial data exists for the tweet. This is to produce interesting data geographical plots and not overwhelm AWS comprehend (free account, not paying for this service!). 

The pipeline is as follows:
1. Source: Twitter (API)
2. Collection: Flume
3. Messaging: Kafka
4. Analysis: Python, AWS Comprehend (boto3)
5. Messaging: Kafka Connect
6. Storage: ElasticSearch
7. Presentation: Kibana

- More about this project can be read in the included doc. file!

### YouTube Vid 

The PI required us to walk through the project via creating a YouTube video. Apologies for the poor quality (360p), and my voice. 
https://youtu.be/oDCv5LeM0ME

### Tech used in Final Project

Twitter API, Flume, Kafka, AWS Comprehend (Python), Kafka Connect (Python), ElasticSearch, Kibana

### Tech used throughout course
Hadoop, HDFS, Redis, MapReduce, Avro, Kafka, Spark (streaming), ElasticSearch, Kibana, NoSQL
**AWS tools**: EMR, EC2, RedShift, CloudFormation

### Course Description
The goal of this course is to learn core principles of building highly distributed, highly available systems for processing large volumes of data with historical and near real-time querying capabilities. We cover the stages of data processing that are common to most real-world systems, including high-volume, high-speed data ingestion, historical and real-time metrics aggregation, techniques to address unique counts, data de-duplication and reprocessing, storage options, distributed data indexing, and search. We review approaches to solving common challenges of such systems and get hands-on experience implementing some of them. We look at trends and the evolution of data processing and analytics with special attention to the modern data stack and the resulting advances in data warehousing, data lakes, and data mesh solutions. The focus of this course is on understanding the challenges and core principles of big data processing, not on specific frameworks or technologies used for implementation. We review a few notable technologies for each area with a deeper dive into a few select ones. The course is structured as a progression of topics covering the full, end-to-end data processing pipeline typical in real-world scenarios.
