provider "aws" {
  region = "sa-east-1"
}
data "aws_caller_identity" "current" {}

data "aws_availability_zones" "azs" {
  state = "available"
}

################# VPC / Subnets / Security Group / KMS Key #################

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
  map_public_ip_on_launch   = true
}

resource "aws_subnet" "subnet_az2" {
  availability_zone = data.aws_availability_zones.azs.names[1] # sa-east-1b
  cidr_block        = "192.168.1.0/24"
  vpc_id            = aws_vpc.vpc.id
  map_public_ip_on_launch   = true
}

resource "aws_subnet" "subnet_az3" {
  availability_zone = data.aws_availability_zones.azs.names[2] # sa-east-1c
  cidr_block        = "192.168.2.0/24"
  vpc_id            = aws_vpc.vpc.id
  map_public_ip_on_launch   = true
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "a1" {
  subnet_id      = aws_subnet.subnet_az1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "a2" {
  subnet_id      = aws_subnet.subnet_az2.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "a3" {
  subnet_id      = aws_subnet.subnet_az3.id
  route_table_id = aws_route_table.public_rt.id
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

################# Cloudwatch Logs / S3 Bucket #################

resource "aws_cloudwatch_log_group" "test" {
  name = "msk_broker_logs"
    retention_in_days = 3
    kms_key_id = aws_kms_key.kms.arn
}

resource "aws_s3_bucket" "bucket" {
  bucket = "smart-prop-msk-broker-logs"
}


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


################# MSK Cluster #################

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


################# EC2 Windows Instance #################

resource "aws_instance" "windows_instance" {
  ami                         = "ami-0d683f13af7e345f0"  # AMI do Windows Server 2022 Base de 
  instance_type               = "t3.xlarge"
  subnet_id                   = aws_subnet.subnet_az1.id
  key_name                    = "master-smart-rsa"       
  vpc_security_group_ids      = [aws_security_group.sg.id]
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 45         # GB
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "smartprop"
  }
}

output "ec2_instance_id" {
  value = aws_instance.windows_instance.id
}