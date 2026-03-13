from pydantic import BaseModel
from typing import Optional


class PokemonType(BaseModel):
    name: str
    url: str


class PokemonStat(BaseModel):
    base_stat: int
    effort: int
    name: str


class PokemonBasic(BaseModel):
    id: int
    name: str
    name_zh: Optional[str] = None
    image_url: str
    types: list[str]
    type_colors: list[str]


class PokemonDetail(BaseModel):
    id: int
    name: str
    name_zh: Optional[str] = None
    image_url: str
    types: list[str]
    type_colors: list[str]
    height: float
    weight: float
    stats: dict[str, int]
    description: Optional[str] = None
    genus: Optional[str] = None


class EvolutionStage(BaseModel):
    id: int
    name: str
    name_zh: Optional[str] = None
    image_url: str
    trigger: Optional[str] = None
    level: Optional[int] = None
    item: Optional[str] = None


class EvolutionChain(BaseModel):
    chain: list[list[EvolutionStage]]
