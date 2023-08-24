from fastapi import FastAPI, Request, Form
import sys
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import socket
import uvicorn
from models import AppSettings
from poke_caller import PokeCaller

settings = AppSettings()
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/test")
async def test():
    return {"message":"this is a test"}

@app.get('/')
async def render_root(request: Request):
    hostname = socket.gethostname()
    return templates.TemplateResponse("index.html",{"request":request,"hostname":hostname}) 

@app.post('/pokemon')
async def render_pokemon(request: Request, pokemon_name: str = Form(...)):
    hostname = socket.gethostname()
    try:
        data = PokeCaller(pokemon_name).poke_data
        weight = data["weight"]
        image = data["image"]
        types = data["types"]
    except Exception as e:
        weight = f"Error: {e}"
        types = "-"
        image = "/static/entonerror.jpg"

    return templates.TemplateResponse("index.html", {"request":request,"hostname":hostname,"pokemon":pokemon_name.capitalize(),"weight":weight,"types":types,"image":image})

if __name__ == "__main__":
    if "dev".lower() in sys.argv:
        print("DEV-Mode")
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=settings.api_port, reload=True)
    else:
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=settings.api_port)