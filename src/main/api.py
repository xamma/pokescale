from fastapi import FastAPI, Request, Form
import sys
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import socket
import uvicorn
from models import AppSettings
from poke_caller import PokeCaller
import logging
from pathlib import Path

# -Logging configuration----------------------------
# create logger
logger = logging.getLogger("API_Logger")
logger.setLevel(logging.INFO)

# create console handler and set level to info
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# -Load Application settings-----------------------
settings = AppSettings()

# -Initialization----------------------------------
app = FastAPI()

# templates and static files directory
BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

templates = Jinja2Templates(directory=TEMPLATE_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -API Area----------------------------------------
# test route
@app.get("/test")
async def test():
    logger.info("Test route called")
    return {"message": "this is a test"}


# render root
@app.get("/")
async def render_root(request: Request):
    logger.info("root route called")
    hostname = socket.gethostname()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"hostname": hostname}
    )


# render pokemon
@app.post("/pokemon")
async def render_pokemon(request: Request, pokemon_name: str = Form(...)):
    logger.info("pokemon route called")
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
        logger.error(f"Failed getting information about Pokemon {pokemon_name}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "hostname": hostname,
            "pokemon": pokemon_name.capitalize(),
            "weight": weight,
            "types": types,
            "image": image,
        },
    )


# -Runner------------------------------------------
if __name__ == "__main__":
    if "dev".lower() in sys.argv:
        logger.info("FastAPI App started in DEV mode")
        uvicorn.run(
            app="__main__:app", host="0.0.0.0", port=settings.api_port, reload=True
        )
    else:
        logger.info("FastAPI App started")
        uvicorn.run(app="__main__:app", host="0.0.0.0", port=settings.api_port)
        logger.info("FastAPI app shut down")
