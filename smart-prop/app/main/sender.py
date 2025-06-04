from kafka import KafkaConsumer
import json

subcontas = {"117", "119"}

consumer = KafkaConsumer(
    'entryorders',
    bootstrap_servers=[
        'b-1.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094',
        'b-2.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094',
        'b-3.smartprop.j12dbs.c4.kafka.sa-east-1.amazonaws.com:9094'
    ],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    security_protocol='SSL'  # Troque PLAINTEXT por SSL
)

    

def process_order_message(msg_str):
    try:
        data = json.loads(msg_str)

        subconta = str(data.get("sub_account_id"))
        if subconta not in subcontas:
            return  

        status = data.get("order_status")
        side = data.get("side")
        ticker = data.get("ticker")
        price = data.get("price")
        quantity = data.get("traded_quantity")

        print(f"\n📨 Nova ordem recebida: {data}")

        if status == "Filled":
            if side == "V":
                print(f" 🚀 Enviando COMPRA {quantity} contratos de {ticker} a mercado")
            elif side == "C":
                print(f" 🚀 Enviando VENDA de {quantity} contratos de {ticker} a mercado")

            return 

    except json.JSONDecodeError:
        print("❌ Erro: mensagem não é um JSON válido")
    except Exception as e:
        print(f"❌ Erro inesperado ao processar mensagem: {e}")

for msg in consumer:
    msg_str = msg.value.decode('utf-8')
    try:
        data = json.loads(msg_str)
        subconta = str(data.get("sub_account_id"))
        if subconta in subcontas:
            process_order_message(msg_str)
    except Exception as e:
        print(f"⚠️ Erro ao processar mensagem Kafka: {e}")