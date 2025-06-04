from getpass import getpass
from ctypes import byref, c_wchar_p, c_double, c_int
from profitTypes import *
from profit_dll import initializeDll
from datetime import datetime
from pyspark.sql import SparkSession
import os

# Caminho dos JARs
jars_path = r"C:\headsystem\head-system\smart-prop\app\jars"
jars_list = ",".join([os.path.join(jars_path, f) for f in os.listdir(jars_path) if f.endswith(".jar")])

# Caminho fixo para o checkpoint
checkpoint_path = r"C:\headsystem\spark_checkpoint"
os.makedirs(checkpoint_path, exist_ok=True)

# Criação da sessão Spark com configs específicas
spark = SparkSession.builder \
    .appName("smartPropGetOrders") \
    .config("spark.jars", jars_list) \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .config("spark.sql.adaptive.enabled", "false") \
    .getOrCreate()

# Leitura do Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "b-1.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-2.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-3.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094") \
    .option("subscribe", "entryorders") \
    .option("startingOffsets", "latest") \
    .option("kafka.security.protocol", "SSL") \
    .load()

df_values = df_kafka.selectExpr("CAST(value AS STRING) as message")

# Escrita no console
query = df_values.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("checkpointLocation", checkpoint_path) \
    .option("truncate", False) \
    .start()

query.awaitTermination()