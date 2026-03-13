from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
TOTAL_POKEMON = 151

TYPE_COLORS = {
    "fire": "#F08030",
    "water": "#6890F0",
    "grass": "#78C850",
    "electric": "#F8D030",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "normal": "#A8A878",
    "steel": "#B8B8D0",
    "dark": "#705848",
    "fairy": "#EE99AC",
}

TYPE_NAMES_ZH = {
    "fire": "火",
    "water": "水",
    "grass": "草",
    "electric": "电",
    "ice": "冰",
    "fighting": "格斗",
    "poison": "毒",
    "ground": "地面",
    "flying": "飞行",
    "psychic": "超能力",
    "bug": "虫",
    "rock": "岩石",
    "ghost": "幽灵",
    "dragon": "龙",
    "normal": "普通",
    "steel": "钢",
    "dark": "恶",
    "fairy": "妖精",
}
