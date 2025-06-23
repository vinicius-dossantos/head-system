import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    Função Lambda que DESLIGA uma instância EC2 específica,
    verificando antes se ela já está parada.

    O ID da instância EC2 será lido do payload do evento, na chave 'instance_id'.
    Exemplo de payload: {'instance_id': 'i-08df3c88554cbd905'}
    """

    instance_id = event.get('instance_id')
    if not instance_id:
        return {
            'statusCode': 400,
            'body': "O payload deve conter a chave 'instance_id'."
        }

    ec2 = boto3.client('ec2')

    try:
        # Verifica o estado atual da instância
        response = ec2.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if state in ['stopping', 'stopped']:
            return {
                'statusCode': 200,
                'body': f"A instância {instance_id} já está em estado '{state}'."
            }

        # Desliga a instância
        ec2.stop_instances(InstanceIds=[instance_id])
        return {
            'statusCode': 200,
            'body': f"Comando para desligar a instância {instance_id} enviado com sucesso."
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': f"Erro do cliente EC2 ao desligar a instância {instance_id}: {e}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Erro inesperado: {e}"
        }