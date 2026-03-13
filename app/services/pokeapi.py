import httpx
import asyncio
from typing import Optional
import logging

from app.config import POKEAPI_BASE_URL, TOTAL_POKEMON, TYPE_COLORS, TYPE_NAMES_ZH
from app.models.pokemon import (
    PokemonBasic,
    PokemonDetail,
    EvolutionStage,
    EvolutionChain,
)

logger = logging.getLogger(__name__)


class PokeAPIClient:
    def __init__(self):
        self.base_url = POKEAPI_BASE_URL
        self._cache: dict = {}
        self._species_cache: dict = {}
        self._evolution_cache: dict = {}
        self._timeout = httpx.Timeout(30.0, connect=30.0)
        self._max_concurrent = 3
        self._semaphore: Optional[asyncio.Semaphore] = None

    async def _get_semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self._max_concurrent)
        return self._semaphore

    async def _fetch_with_retry(
        self, client: httpx.AsyncClient, url: str, max_retries: int = 5
    ) -> dict:
        semaphore = await self._get_semaphore()
        async with semaphore:
            for attempt in range(max_retries):
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.json()
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = 3 * (attempt + 1)
                        logger.warning(f"Retry {attempt + 1}/{max_retries} for {url}: {type(e).__name__}")
                        await asyncio.sleep(wait_time)
                        continue
                    logger.error(f"Failed to fetch {url} after {max_retries} retries: {e}")
                    raise e
            raise Exception(f"Failed to fetch {url} after {max_retries} retries")

    async def get_pokemon(self, pokemon_id: int) -> dict:
        if pokemon_id in self._cache:
            return self._cache[pokemon_id]

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            url = f"{self.base_url}/pokemon/{pokemon_id}"
            data = await self._fetch_with_retry(client, url)
            self._cache[pokemon_id] = data
            return data

    async def get_species(self, pokemon_id: int) -> dict:
        if pokemon_id in self._species_cache:
            return self._species_cache[pokemon_id]

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            url = f"{self.base_url}/pokemon-species/{pokemon_id}"
            data = await self._fetch_with_retry(client, url)
            self._species_cache[pokemon_id] = data
            return data

    async def get_evolution_chain(self, chain_id: int) -> dict:
        if chain_id in self._evolution_cache:
            return self._evolution_cache[chain_id]

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            url = f"{self.base_url}/evolution-chain/{chain_id}"
            data = await self._fetch_with_retry(client, url)
            self._evolution_cache[chain_id] = data
            return data

    def _get_chinese_name(self, species_data: dict) -> Optional[str]:
        for name_info in species_data.get("names", []):
            if name_info.get("language", {}).get("name") == "zh-Hans":
                return name_info.get("name")
        return None

    def _get_description(self, species_data: dict) -> Optional[str]:
        for flavor in species_data.get("flavor_text_entries", []):
            if flavor.get("language", {}).get("name") == "zh-Hans":
                text = flavor.get("flavor_text", "")
                return text.replace("\n", " ").replace("\f", " ")
        for flavor in species_data.get("flavor_text_entries", []):
            if flavor.get("language", {}).get("name") == "en":
                text = flavor.get("flavor_text", "")
                return text.replace("\n", " ").replace("\f", " ")
        return None

    def _get_genus(self, species_data: dict) -> Optional[str]:
        for genus_info in species_data.get("genera", []):
            if genus_info.get("language", {}).get("name") == "zh-Hans":
                return genus_info.get("genus")
        return None

    async def get_pokemon_basic(self, pokemon_id: int) -> PokemonBasic:
        pokemon_data = await self.get_pokemon(pokemon_id)
        species_data = await self.get_species(pokemon_id)

        types = [t["type"]["name"] for t in pokemon_data["types"]]
        type_colors = [TYPE_COLORS.get(t, "#A8A878") for t in types]

        return PokemonBasic(
            id=pokemon_id,
            name=pokemon_data["name"],
            name_zh=self._get_chinese_name(species_data),
            image_url=pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
            or pokemon_data["sprites"]["front_default"],
            types=types,
            type_colors=type_colors,
        )

    async def get_pokemon_detail(self, pokemon_id: int) -> PokemonDetail:
        pokemon_data = await self.get_pokemon(pokemon_id)
        species_data = await self.get_species(pokemon_id)

        types = [t["type"]["name"] for t in pokemon_data["types"]]
        type_colors = [TYPE_COLORS.get(t, "#A8A878") for t in types]

        stats = {}
        for stat in pokemon_data["stats"]:
            stat_name = stat["stat"]["name"]
            stats[stat_name] = stat["base_stat"]

        return PokemonDetail(
            id=pokemon_id,
            name=pokemon_data["name"],
            name_zh=self._get_chinese_name(species_data),
            image_url=pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
            or pokemon_data["sprites"]["front_default"],
            types=types,
            type_colors=type_colors,
            height=pokemon_data["height"] / 10,
            weight=pokemon_data["weight"] / 10,
            stats=stats,
            description=self._get_description(species_data),
            genus=self._get_genus(species_data),
        )

    async def get_evolution_chain_for_pokemon(self, pokemon_id: int) -> EvolutionChain:
        species_data = await self.get_species(pokemon_id)
        chain_url = species_data.get("evolution_chain", {}).get("url", "")
        if not chain_url:
            return EvolutionChain(chain=[])

        chain_id = chain_url.rstrip("/").split("/")[-1]
        chain_data = await self.get_evolution_chain(int(chain_id))

        chain_stages = self._parse_evolution_chain(chain_data["chain"])
        return EvolutionChain(chain=chain_stages)

    def _parse_evolution_chain(self, chain_data: dict) -> list[list[EvolutionStage]]:
        result: list[list[EvolutionStage]] = []
        self._traverse_chain(chain_data, result, 0)
        return result

    def _traverse_chain(
        self,
        chain_data: dict,
        result: list[list[EvolutionStage]],
        stage: int,
        trigger: Optional[str] = None,
        level: Optional[int] = None,
        item: Optional[str] = None,
    ):
        pokemon_id = int(chain_data["species"]["url"].rstrip("/").split("/")[-1])

        while len(result) <= stage:
            result.append([])

        evolution_stage = EvolutionStage(
            id=pokemon_id,
            name=chain_data["species"]["name"],
            name_zh=None,
            image_url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png",
            trigger=trigger,
            level=level,
            item=item,
        )
        result[stage].append(evolution_stage)

        for evolves_to in chain_data.get("evolves_to", []):
            evolution_details = evolves_to.get("evolution_details", [{}])
            if evolution_details:
                details = evolution_details[0]
                next_trigger = details.get("trigger", {}).get("name") if details.get("trigger") else None
                next_level = details.get("min_level")
                next_item = details.get("item", {}).get("name") if details.get("item") else None
            else:
                next_trigger = None
                next_level = None
                next_item = None

            self._traverse_chain(
                evolves_to, result, stage + 1, next_trigger, next_level, next_item
            )

    async def get_all_pokemon_basic(self) -> list[PokemonBasic]:
        results = []
        for i in range(1, TOTAL_POKEMON + 1):
            try:
                pokemon = await self.get_pokemon_basic(i)
                results.append(pokemon)
                if i % 10 == 0:
                    logger.info(f"Loaded {i}/{TOTAL_POKEMON} pokemon")
            except Exception as e:
                logger.error(f"Failed to load pokemon {i}: {e}")
                raise e
        return results


pokeapi_client = PokeAPIClient()
