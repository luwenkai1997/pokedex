from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.routers import pokemon

app = FastAPI(
    title="Pokedex",
    description="A web application for the first 151 Pokemon",
    version="0.1.0",
)

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(pokemon.router)
