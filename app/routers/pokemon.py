from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.pokeapi import pokeapi_client
from app.config import TYPE_COLORS, TYPE_NAMES_ZH

router = APIRouter()

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "type_colors": TYPE_COLORS,
            "type_names_zh": TYPE_NAMES_ZH,
        },
    )


@router.get("/pokemon/{pokemon_id}", response_class=HTMLResponse)
async def pokemon_detail(request: Request, pokemon_id: int):
    if pokemon_id < 1 or pokemon_id > 151:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "pokemon_id": pokemon_id,
            "type_colors": TYPE_COLORS,
            "type_names_zh": TYPE_NAMES_ZH,
        },
    )


@router.get("/api/pokemon")
async def get_all_pokemon():
    pokemon_list = await pokeapi_client.get_all_pokemon_basic()
    return {"pokemon": [p.model_dump() for p in pokemon_list]}


@router.get("/api/pokemon/{pokemon_id}")
async def get_pokemon(pokemon_id: int):
    if pokemon_id < 1 or pokemon_id > 151:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    detail = await pokeapi_client.get_pokemon_detail(pokemon_id)
    evolution = await pokeapi_client.get_evolution_chain_for_pokemon(pokemon_id)

    evolution_with_names = []
    for stage in evolution.chain:
        stage_with_names = []
        for evo in stage:
            species_data = await pokeapi_client.get_species(evo.id)
            evo.name_zh = pokeapi_client._get_chinese_name(species_data)
            stage_with_names.append(evo.model_dump())
        evolution_with_names.append(stage_with_names)

    return {
        "pokemon": detail.model_dump(),
        "evolution": evolution_with_names,
    }


@router.get("/api/types")
async def get_types():
    return {
        "types": list(TYPE_COLORS.keys()),
        "colors": TYPE_COLORS,
        "names_zh": TYPE_NAMES_ZH,
    }
