variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami" {
  default = "ami-080e1f13689e07408"
}

variable "key_name" {
  default = "AWS_SSH_PRIVATE_KEY"
}

variable "docker_image" {
  default = "ronierisonmaciel/login-app:latest"
}
