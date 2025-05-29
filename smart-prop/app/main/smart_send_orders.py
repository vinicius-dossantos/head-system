#Imports para execução da DLL
import ctypes
from getpass import getpass
from ctypes import *
import struct
from datetime import *
from confluent_kafka import Producer
from profitTypes import *
from profit_dll import initializeDll
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
import os
from broker import ProfitOrderSender


profit_dll = initializeDll(r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\DLLs\Win64\ProfitDLL.dll")

jar_dir = r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\Exemplo Python\jars"
jars = [
    "spark-sql-kafka-0-10_2.12-3.5.0.jar",
    "kafka-clients-3.5.1.jar",
    "spark-token-provider-kafka-0-10_2.12-3.5.0.jar",
    "commons-pool2-2.11.1.jar"
]
jars_paths = ",".join([os.path.join(jar_dir, jar).replace("\\", "/") for jar in jars])

json_schema = StructType() \
    .add("load_dt_hr", StringType()) \
    .add("dt_criacao_str", StringType()) \
    .add("dt_execucao_str", StringType()) \
    .add("ticker", StringType()) \
    .add("traded_quantity", IntegerType()) \
    .add("side", StringType()) \
    .add("price", DoubleType()) \
    .add("account_id", StringType()) \
    .add("sub_account_id", StringType()) \
    .add("cl_order_id", StringType()) \
    .add("order_status_code", IntegerType()) \
    .add("order_status", StringType()) \
    .add("order_type", StringType()) \
    .add("message", StringType())

spark = SparkSession.builder \
    .appName("Kafka EntryOrders Consumer")  \
    .config("spark.jars", ",".join([
        r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\Exemplo Python\jars\spark-sql-kafka-0-10_2.12-3.5.0.jar",
        r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\Exemplo Python\jars\kafka-clients-3.5.1.jar",
        r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\Exemplo Python\jars\spark-token-provider-kafka-0-10_2.12-3.5.0.jar",
        r"C:\Users\vinic\OneDrive\Documentos\GitHub\smart-prop-ORH\doc\ProfitDLL\Exemplo Python\jars\commons-pool2-2.11.1.jar"
    ])) \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.executor.memory", "6g") \
    .config("spark.executor.cores", "4") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
#spark.sparkContext.setLogLevel("INFO")

df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "entryorders") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", 1000) \
    .option("minPartitions", 4) \
    .load()

# Conversão de value para JSON + extração das colunas + timestamp de ingestão
df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_str") \
    .withColumn("data", from_json(col("json_str"), json_schema)) \
    .select("data.*") \
    .withColumn("ingestion_timestamp", current_timestamp())

# Impressão no console
query = df_parsed.writeStream \
    .format("console") \
    .option("truncate", False) \
    .trigger(processingTime="0 milliseconds") \
    .start()

query.awaitTermination()