variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami" {
  default = "ami-084568db4383264d4"
}

variable "key_name" {
  default = "macOS"
}

variable "docker_image" {
  default = "ronierisonmaciel/login-app:latest"
}
