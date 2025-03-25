from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes import user_router
from core.container import Container

app = FastAPI()

container = Container()
container.init_resources()
app.container = container  # Adiciona o container ao FastAPI

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router.router)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
def read_root():
    return {"message": "API com Arquitetura Hexagonal! "}
