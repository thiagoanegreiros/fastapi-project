from fastapi import FastAPI
from core.container import Container
from api.routes import user_router

app = FastAPI()

container = Container()
container.init_resources()
app.container = container  # Adiciona o container ao FastAPI

app.include_router(user_router.router)

@app.get("/")
def read_root():
    return {"message": "API com Arquitetura Hexagonal!"}
