from getpass import getpass
from ctypes import byref, c_wchar_p, c_double, c_int
from profitTypes import *
from profit_dll import initializeDll
from datetime import datetime
from pyspark.sql import SparkSession
import os

jars_path = r"C:\headsystem\head-system\smart-prop\app\jars"
jars_list = ",".join([os.path.join(jars_path, f) for f in os.listdir(jars_path) if f.endswith(".jar")])

spark = SparkSession.builder \
    .appName("smartPropGetOrders") \
    .config("spark.jars", jars_list) \
    .getOrCreate()

df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "b-1.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-2.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-3.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094") \
    .option("subscribe", "entryorders") \
    .option("startingOffsets", "latest") \
    .option("kafka.security.protocol", "SSL") \
    .load()

df_values = df_kafka.selectExpr("CAST(value AS STRING) as message")

query = df_values.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()