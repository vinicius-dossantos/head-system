from getpass import getpass
from ctypes import byref, c_wchar_p, c_double, c_int
from profitTypes import *
from profit_dll import initializeDll
from datetime import datetime
from pyspark.sql import SparkSession
import os

# Define o interpretador Python explicitamente (opcional, mas pode evitar warnings)
os.environ["PYSPARK_PYTHON"] = "C:/Program Files/Python310/python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = "C:/Program Files/Python310/python.exe"

# Caminho dos JARs
jars_path = r"C:\headsystem\head-system\smart-prop\app\jars"
jars_list = ",".join([os.path.join(jars_path, f) for f in os.listdir(jars_path) if f.endswith(".jar")])

# Caminho do checkpoint
checkpoint_path = r"C:\headsystem\spark_checkpoint"
os.makedirs(checkpoint_path, exist_ok=True)

# Criação da sessão Spark
spark = SparkSession.builder \
    .appName("smartPropGetOrders") \
    .config("spark.jars", jars_list) \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .config("spark.sql.adaptive.enabled", "false") \
    .getOrCreate()

# Lê dados do Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "b-1.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-2.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094,b-3.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094") \
    .option("subscribe", "entryorders") \
    .option("startingOffsets", "earliest") \
    .option("kafka.security.protocol", "SSL") \
    .option("maxOffsetsPerTrigger", 1) \
    .load()

# Converte o valor para string e garante 1 partição (sequencial)
df_values = df_kafka.selectExpr("CAST(value AS STRING) as message")
#df_values = df_kafka.selectExpr("CAST(value AS STRING) as message").repartition(1)

# Função para imprimir cada mensagem individualmente
def process_batch(df, batch_id):
    print(f"\n🔄 Processando lote {batch_id} - {df.count()} mensagens")
    rows = df.collect()
    for row in rows:
        print(f"[Kafka Message - Batch {batch_id}] {row['message']}")

# Escrita com foreachBatch para controle total
query = df_values.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", checkpoint_path) \
    .start()

query.awaitTermination()