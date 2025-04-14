# 🖥️ FastAPI Login App - Deploy Automatizado com Terraform e GitHub Actions na AWS

Este projeto demonstra como fazer o **deploy automatizado** de uma aplicação web simples em **FastAPI**, utilizando **Terraform** com backend remoto na AWS (S3 + DynamoDB) e **GitHub Actions** para CI/CD, com execução final em uma **instância EC2 com Docker**.

---

## 🚀 Funcionalidades

- Aplicação de login com validação simples (`admin/1234`)
- Deploy automático com GitHub Actions ao alterar o código
- Provisionamento de infraestrutura na AWS com Terraform
- Armazenamento remoto do estado no S3 com lock via DynamoDB
- Evita reconstrução de instância se não houver alterações no Terraform
- Execução da aplicação em contêiner Docker na EC2

---

## 📁 Estrutura do Projeto

```
projeto-login-aws/
├── app/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── .github/
    └── workflows/
        └── deploy.yml      # Workflow unificado (infra + app)
```

---

## 🔧 Pré-requisitos

- [Docker](https://app.docker.com/)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Conta no [Docker Hub](https://hub.docker.com/)
- Conta na [AWS](https://aws.amazon.com/)

---

## 🐳 Criando e publicando a imagem Docker

```bash
cd app
docker build -t SEU_USUARIO_DOCKER/login-app:latest .
docker login
docker push SEU_USUARIO_DOCKER/login-app:latest
```

---

## ☁️ Criando uma chave SSH na AWS

1. Acesse AWS Console → EC2 → **Key Pairs**
2. Crie uma nova chave no formato `.pem` e salve localmente
3. Anote o nome (ex.: `fastapi-key`) para usar no Terraform

---

## 🛠️ Configurando o backend remoto no Terraform

> A configuração abaixo server para resolver o problema da criação de uma nova instância a cada alteração no projeto. Mas lembre-se! Tem que alterar o arquivo `deploy-aws.yml` no workflow, deixei o source na raiz do repositório, caso haja interesse `deploy.yml`.

No arquivo `main.tf`:

```hcl
terraform {
  backend "s3" {
    bucket         = "meu-bucket-terraform"     # Substitua pelo nome real do bucket
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

Crie os recursos com:

```bash
aws s3api create-bucket --bucket meu-bucket-terraform --region us-east-1

aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

---

## ✍️ Configurando variáveis do Terraform

No arquivo `variables.tf`:

```hcl
variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami" {
  default = "ami-084568db4383264d4"  # Ubuntu Server 22.04 LTS
}

variable "key_name" {
  default = "fastapi-key"
}

variable "docker_image" {
  default = "SEU_USUARIO_DOCKER/login-app:latest"
}
```

---

## 🔐 Configurando Secrets no GitHub

Acesse seu repositório no GitHub:

> **Settings → Secrets and variables → Actions → New repository secret**

Adicione os seguintes:

| Nome                   | Valor                                                         |
|------------------------|---------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID`    | Chave de acesso da AWS                                        |
| `AWS_SECRET_ACCESS_KEY`| Chave secreta da AWS                                          |
| `AWS_SSH_PRIVATE_KEY`  | Conteúdo da chave `.pem` criada na AWS                        |

---

## 🔄 Fluxo de Deploy com GitHub Actions (`deploy.yml`)

- Executado em **todo push na branch `main`**
- Detecta alterações em `terraform/` e executa `terraform apply` apenas se necessário
- Estado da infraestrutura é armazenado em S3 (persistente entre execuções)
- IP público é obtido com validação robusta
- Código da aplicação é copiado via SCP e executado via SSH na EC2

---

## 🌐 Acessando a aplicação

Após o deploy, acesse:

```
http://<IP_PÚBLICO_DA_INSTÂNCIA>
```

### 📥 Login de exemplo

| Usuário | Senha |
|---------|-------|
| admin   | 1234  |

---

## 🧨 Remover recursos da AWS

Para destruir a infraestrutura provisionada:

```bash
cd terraform
terraform destroy -auto-approve
```

---

## 🛠️ Possíveis erros e soluções

| Erro                                                              | Solução                                                                 |
|-------------------------------------------------------------------|-------------------------------------------------------------------------|
| `InvalidGroup.Duplicate`                                          | Agora evitado com backend remoto no S3                                 |
| `connection refused` no SSH                                       | Adicione `sleep 60` antes do SSH no GitHub Actions                     |
| `unable to authenticate` no SSH                                   | Verifique se a chave privada no GitHub bate com a pública na AWS       |
| `terraform output -raw ec2_public_ip` falha                       | Agora tratado com verificação robusta no workflow                      |
| Container reiniciando mesmo sem mudanças                          | Pode ser otimizado usando `docker pull` e imagens versionadas          |

---

## 👨‍💻 Autor

Desenvolvido por **Ronierison Maciel**  
📧 [LinkedIn](https://linkedin.com/in/ronierisonmaciel) | [GitHub](https://github.com/ronierisonmaciel)
