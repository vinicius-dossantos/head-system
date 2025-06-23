import boto3
import os

def lambda_handler(event, context):
    """
    Função Lambda que inicia uma instância EC2 específica,
    verificando antes se ela já não está rodando.

    O ID da instância EC2 será lido do payload do evento, na chave 'instance_id'.
    Exemplo de payload: {'instance_id': 'i-08df3c88554cbd905'}
    """
    
    # Obtém o ID da instância EC2 do payload do evento
    # Usamos .get() para evitar KeyError se a chave não existir e fornecer um valor padrão (None)
    instance_id = event.get('instance_id')

    if not instance_id:
        print("Erro: 'instance_id' não foi fornecido no payload do evento.")
        # Retorna um erro se o ID da instância não estiver no payload
        return {
            'statusCode': 400,
            'body': "Parâmetro 'instance_id' ausente no payload do evento."
        }

    # Inicializa o cliente EC2 do boto3.
    ec2 = boto3.client('ec2')

    try:
        print(f"Verificando o status da instância EC2 com ID: {instance_id}...")
        
        # Descreve a instância para obter seu status atual
        response = ec2.describe_instances(InstanceIds=[instance_id])
        
        # Verifica se a instância foi encontrada e obtém seu estado
        reservations = response['Reservations']
        if not reservations or not reservations[0]['Instances']:
            print(f"Erro: Instância {instance_id} não encontrada ou não tem informações de instância.")
            return {
                'statusCode': 404,
                'body': f'Instância {instance_id} não encontrada.'
            }
        
        instance_state = reservations[0]['Instances'][0]['State']['Name']
        print(f"Status atual da instância {instance_id}: {instance_state}")
        
        # Verifica se a instância já está rodando ou está em processo de inicialização
        if instance_state == 'running':
            print(f"A instância {instance_id} já está rodando. Nenhuma ação necessária.")
            return {
                'statusCode': 200,
                'body': f'Instância {instance_id} já está rodando.'
            }
        elif instance_state == 'pending':
            print(f"A instância {instance_id} está no estado 'pending' (inicializando). Aguardando...")
            return {
                'statusCode': 200,
                'body': f'Instância {instance_id} já está inicializando.'
            }
        
        # Se o status não for 'running' nem 'pending', tentar iniciar
        print(f"A instância {instance_id} está no estado '{instance_state}'. Tentando iniciar...")
        start_response = ec2.start_instances(InstanceIds=[instance_id])
        
        print(f"Comando de início enviado com sucesso para a instância: {instance_id}")
        print("Resposta detalhada da AWS:", start_response)
        
        return {
            'statusCode': 200,
            'body': f'Instância {instance_id} iniciada com sucesso.'
        }
        
    except ec2.exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "InvalidInstanceID.NotFound":
            print(f"Erro: Instância {instance_id} não existe ou está em uma região diferente. Detalhes: {e}")
            return {
                'statusCode': 404,
                'body': f'Instância {instance_id} não encontrada ou inválida: {str(e)}'
            }
        else:
            print(f"Erro do cliente EC2 ao processar a instância {instance_id}: {e}")
            return {
                'statusCode': 500,
                'body': f'Erro do cliente EC2 ao iniciar a instância {instance_id}: {str(e)}'
            }
    except Exception as e:
        print(f"Erro inesperado ao processar a instância {instance_id}: {e}")
        return {
            'statusCode': 500,
            'body': f'Erro inesperado ao iniciar a instância {instance_id}: {str(e)}'
        }
