provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data_lake" {
  bucket = "my-company-data-lake"
  
  # 🚨 FALLO: Bucket público (Cebo para Checkov/Trivy)
  acl    = "public-read"

  versioning {
    enabled = false # 🚨 FALLO: Sin versionado
  }
}

resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    # 🚨 FALLO: Abierto a todo internet
    cidr_blocks = ["0.0.0.0/0"]
  }
}