from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

USUARIO = "admin"
SENHA = "1234"

@app.get("/", response_class=HTMLResponse)
async def pagina_login():
    return """
    <h1 style='color:red;'>Login</h1><br />
    <form method="post">
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
