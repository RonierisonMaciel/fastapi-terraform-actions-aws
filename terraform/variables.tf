variable "region" {
  default = "us-east-1"
}

variable "ami_id" {
  default = "ami-080e1f13689e07408" # Ubuntu Server 22.04 LTS
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_pair" {
  description = "macOS"
  type        = string
}

variable "docker_image" {
  description = "Imagem Docker pública do DockerHub"
  type        = string
}
