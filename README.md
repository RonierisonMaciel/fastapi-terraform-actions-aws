# 🖥️ FastAPI Login App - Deploy Automatizado com Terraform e GitHub Actions na AWS

Este projeto demonstra como fazer o deploy automatizado de uma aplicação web simples em **FastAPI** usando **Terraform** para provisionamento de infraestrutura e **GitHub Actions** para CI/CD, diretamente na **AWS EC2**.

---

## 🚀 Funcionalidades

- Aplicação de login com validação simples (`admin/1234`)
- Deploy automático com GitHub Actions
- Provisionamento de infraestrutura na AWS com Terraform
- Execução da aplicação em contêiner Docker

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
        └── deploy.yml
```

---

## 🔧 Pré-requisitos

Na sua máquina:

- [Docker](https://www.docker.com/)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Conta no [Docker Hub](https://hub.docker.com/)
- Conta na [AWS](https://aws.amazon.com/)

---

## 🐳 Criando a imagem Docker

1. Acesse a pasta `app`:
   ```bash
   cd app
   ```

2. Construa a imagem localmente:
   ```bash
   docker build -t SEU_USUARIO_DOCKER/login-app:latest .
   ```

3. Faça login no Docker Hub:
   ```bash
   docker login
   ```

4. Envie a imagem:
   ```bash
   docker push SEU_USUARIO_DOCKER/login-app:latest
   ```

---

## ☁️ Criando chave SSH na AWS

1. Vá ao Console AWS → EC2 → **Key Pairs** → **Create Key Pair**
2. Escolha o formato `.pem` e **salve o arquivo**
3. Anote o nome da chave (ex.: `fastapi-key`)

---

## ✍️ Variáveis do Terraform (`terraform/variables.tf`)

Atualize conforme necessário:

```hcl
variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ami" {
  default = "ami-084568db4383264d4"  # Ubuntu Server 22.04 LTS (verifique se está disponível na região escolhida)
}

variable "key_name" {
  default = "fastapi-key"  # Nome da chave criada na AWS
}

variable "docker_image" {
  default = "SEU_USUARIO_DOCKER/login-app:latest"
}
```

---

## 🔐 Secrets no GitHub

No seu repositório GitHub, vá em:  
**Settings → Secrets and variables → Actions → New repository secret**

Adicione os seguintes secrets:

| Nome                  | Valor                                                         |
|-----------------------|---------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID`   | Sua chave de acesso da AWS                                    |
| `AWS_SECRET_ACCESS_KEY` | Sua chave secreta da AWS                                  |
| `AWS_SSH_PRIVATE_KEY` | **Conteúdo da chave `.pem` criada na AWS** (copie e cole!)   |

---

## 🔄 Workflow GitHub Actions

- Toda vez que você fizer `git push` para o branch `main`, o seguinte será executado:

  1. Terraform vai provisionar a instância EC2
  2. A imagem Docker será instalada e executada na instância
  3. A aplicação será disponibilizada no IP público da instância

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

## 🧨 Destruir recursos

Para evitar cobrança na AWS, rode:

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
| `terraform output -raw ec2_public_ip` falha                       | Adicione o bloco de `output` em `outputs.tf`                           |

---

## 👨‍💻 Autor

Desenvolvido por **Ronierison Maciel**  
📧 [LinkedIn](https://linkedin.com/in/ronierisonmaciel) | [GitHub](https://github.com/ronierisonmaciel)
