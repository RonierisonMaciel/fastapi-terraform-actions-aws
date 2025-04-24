from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

USUARIO = "admin"
SENHA = "1234"

@app.get("/", response_class=HTMLResponse)
async def pagina_login():
    return """
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        h1 {
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
            width: 200px;
            margin: auto;
        }
        input {
            margin-bottom: 10px;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
    <script>
        function validarFormulario() {
            var usuario = document.forms["loginForm"]["usuario"].value;
            var senha = document.forms["loginForm"]["senha"].value;
            if (usuario == "" || senha == "") {
                alert("Usuário e senha devem ser preenchidos!");
                return false;
            }
        }
    </script>
    <h1 style="text-align: center;"> Login</h1><br />
    <form name="loginForm" method="post" onsubmit="return validarFormulario();">
        <input name="usuario" placeholder="Usuário" />
        <input name="senha" type="password" placeholder="Senha" />
        <button type="submit">Entrar</button>
    </form>
    """

@app.post("/", response_class=HTMLResponse)
async def autenticar(usuario: str = Form(), senha: str = Form()):
    if usuario == USUARIO and senha == SENHA:
        return "<h2 style='color:green;'>Login realizado com sucesso!</h2> <br /> <a href='/'>Sair</a>"
    return "<h2 style='color:red;'>Usuário ou senha incorretos!</h2> <br /> <a href='/'>Tentar novamente</a>"
