# 🖥️ FastAPI Login App - Deploy Automatizado com Terraform e GitHub Actions na AWS

Este projeto demonstra como fazer o **deploy automatizado** de uma aplicação web simples em **FastAPI**, utilizando **Terraform** para provisionamento de infraestrutura e **GitHub Actions** para CI/CD, com execução final na **AWS EC2** com Docker.

---

## 🚀 Funcionalidades

- Aplicação de login com validação simples (`admin/1234`)
- Deploy automático com GitHub Actions ao alterar o código
- Provisionamento de instância EC2 com Terraform
- Execução da aplicação em contêiner Docker
- Verificação de alterações no código (via hash) antes de redeploy
- Workflows separados para infraestrutura e aplicação

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
        ├── infra.yml     # Provisionamento da infraestrutura
        └── app.yml       # Deploy da aplicação
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

## ✍️ Configurando variáveis no Terraform

Edite `terraform/variables.tf` conforme sua configuração:

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
| `AWS_SSH_PRIVATE_KEY`  | Conteúdo da chave `.pem` criada na AWS (copie e cole no campo) |

---

## 🔄 Fluxo de Deploy com GitHub Actions

### ✅ `infra.yml` — Infraestrutura

- Executado quando arquivos em `terraform/**` forem alterados ou via botão manual
- Cria ou atualiza a instância EC2 com Terraform
- Aplica mudanças apenas se detectadas com `terraform plan`

### ✅ `app.yml` — Aplicação

- Executado somente quando arquivos em `app/**` forem alterados
- Verifica hash do código para evitar deploys desnecessários
- Recria o container Docker apenas se houver alterações no código
- Faz o deploy automaticamente na instância EC2 já provisionada

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
| `InvalidGroup.Duplicate`                                          | Altere o nome do Security Group no `main.tf`                           |
| `connection refused` no SSH                                       | Adicione `sleep 60` antes do SSH no GitHub Actions                     |
| `unable to authenticate` no SSH                                   | Verifique se a chave privada no GitHub bate com a chave pública na AWS |
| `terraform output -raw ec2_public_ip` falha                       | Adicione o bloco de `output` corretamente em `outputs.tf`              |
| Container reiniciando mesmo sem mudanças                          | Agora evitado com verificação de hash do código                        |

---

## 👨‍💻 Autor

Desenvolvido por **Ronierison Maciel**  
📧 [LinkedIn](https://linkedin.com/in/ronierisonmaciel) | [GitHub](https://github.com/ronierisonmaciel)
