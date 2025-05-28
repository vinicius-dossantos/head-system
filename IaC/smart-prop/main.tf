provider "aws" {
  region = "sa-east-1"
}
data "aws_caller_identity" "current" {}

data "aws_availability_zones" "azs" {
  state = "available"
}

resource "aws_vpc" "vpc" {
  cidr_block = "192.168.0.0/22"

  tags = {
    Name = "vpc-sp"
  }
}

resource "aws_subnet" "subnet_az1" {
  availability_zone = data.aws_availability_zones.azs.names[0] # sa-east-1a
  cidr_block        = "192.168.0.0/24"
  vpc_id            = aws_vpc.vpc.id
}

resource "aws_subnet" "subnet_az2" {
  availability_zone = data.aws_availability_zones.azs.names[1] # sa-east-1b
  cidr_block        = "192.168.1.0/24"
  vpc_id            = aws_vpc.vpc.id
}

resource "aws_subnet" "subnet_az3" {
  availability_zone = data.aws_availability_zones.azs.names[2] # sa-east-1c
  cidr_block        = "192.168.2.0/24"
  vpc_id            = aws_vpc.vpc.id
}

resource "aws_security_group" "sg" {
  name   = "smart_prop_sg"
  vpc_id = aws_vpc.vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_kms_key" "kms" {
  description = "smart-prop-kms-key"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "Allow CloudWatch Logs",
        Effect    = "Allow",
        Principal = {
          Service = "logs.sa-east-1.amazonaws.com"
        },
        Action    = [
          "kms:Encrypt*",
          "kms:Decrypt*",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ],
        Resource  = "*"
      },
      {
        Sid      = "Allow IAM user access",
        Effect   = "Allow",
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        Action   = "kms:*",
        Resource = "*"
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "test" {
  name = "msk_broker_logs"
    retention_in_days = 3
    kms_key_id = aws_kms_key.kms.arn
}

resource "aws_s3_bucket" "bucket" {
  bucket = "smart-prop-msk-broker-logs"
}

#resource "aws_s3_bucket_acl" "bucket_acl" {
#  bucket = aws_s3_bucket.bucket.id
#  acl    = "private"
#}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

#resource "aws_iam_role" "firehose_role" {
#  name               = "firehose_test_role"
#  assume_role_policy = data.aws_iam_policy_document.assume_role.json
#}

#resource "aws_kinesis_firehose_delivery_stream" "test_stream" {
#  name        = "terraform-kinesis-firehose-msk-broker-logs-stream"
#  destination = "extended_s3"

#  extended_s3_configuration {
#    role_arn   = aws_iam_role.firehose_role.arn
#    bucket_arn = aws_s3_bucket.bucket.arn
#  }

#  tags = {
#    LogDeliveryEnabled = "placeholder"
#  }

#  lifecycle {
#    ignore_changes = [
#      tags["LogDeliveryEnabled"],
#    ]
#  }
#}

resource "aws_msk_cluster" "smartprop" {
  cluster_name           = "smartprop"
  kafka_version          = "3.2.0"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type = "kafka.t3.small"
    client_subnets = [
      aws_subnet.subnet_az1.id,
      aws_subnet.subnet_az2.id,
      aws_subnet.subnet_az3.id,
    ]
    storage_info {
      ebs_storage_info {
        volume_size = 50 # Size in GB
      }
    }
    security_groups = [aws_security_group.sg.id]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = aws_kms_key.kms.arn
  }

  open_monitoring {
    prometheus {
      jmx_exporter {
        enabled_in_broker = true
      }
      node_exporter {
        enabled_in_broker = true
      }
    }
  }

logging_info {
  broker_logs {
    cloudwatch_logs {
      enabled = false
    }
    s3 {
      enabled = false
    }
  }
}

#  logging_info {
#    broker_logs {
#      cloudwatch_logs {
#        enabled   = true
#        log_group = aws_cloudwatch_log_group.test.name
#      }
#      firehose {
#        enabled         = true
#        delivery_stream = aws_kinesis_firehose_delivery_stream.test_stream.name
#      }
#      s3 {
#        enabled = true
#        bucket  = aws_s3_bucket.bucket.id
#        prefix  = "logs/msk-"
#      }
#    }
#  }

  tags = {
    foo = "head-smart-prop"
  }
}

output "zookeeper_connect_string" {
  value = aws_msk_cluster.smartprop.zookeeper_connect_string
}

output "bootstrap_brokers_tls" {
  description = "TLS connection host:port pairs"
  value       = aws_msk_cluster.smartprop.bootstrap_brokers_tls
}

#data "aws_vpc" "vpc_sp" {
#  filter {
#    name   = "tag:Name"
#    values = ["vpc-sp"]
#  }
#}

#data "aws_subnet" "subnet_az1" {
#  filter {
#    name   = "tag:Name"
#    values = ["subnet_az1"]
#  }
#}

#data "aws_subnet" "subnet_az2" {
#  filter {
#    name   = "tag:Name"
#    values = ["subnet_az2"]
#  }
#}

#data "aws_subnet" "subnet_az3" {
#  filter {
#    name   = "tag:Name"
#    values = ["subnet_az3"]
#  }
#}


### GERAR A CHAVE NO TERMINAL ANTES ###
#openssl genrsa -out smart-prop-key.pem 2048
#chmod 400 smart-prop-key.pem
#ssh-keygen -y -f smart-prop-key.pem > smart-prop-key.pub

resource "aws_key_pair" "smart_prop_key" {
  key_name   = "smart-prop-key-pair"
  public_key = file("~/.ssh/id_rsa.pub")
}

data "aws_ami" "windows" {
  most_recent = true
  owners      = ["801119661308"] # Conta oficial da Amazon

  filter {
    name   = "name"
    values = ["Windows_Server-2022-English-Core-Base-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "windows_instance" {
  ami           = data.aws_ami.windows.id
  instance_type = "t3.xlarge"
  subnet_id     = aws_subnet.subnet_az1.id
  key_name      = aws_key_pair.smart_prop_key.key_name
  vpc_security_group_ids = [aws_security_group.sg.id]

  associate_public_ip_address = true

  root_block_device {
    volume_size           = 30         # 30 GB
    volume_type           = "gp3"      # SSD padrão moderno
    delete_on_termination = true       # Apaga o volume ao destruir a instância
  }

  tags = {
    Name = "windows-ec2-smartprop"
  }
}