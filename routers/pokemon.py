from fastapi import APIRouter
from pandas import Series, read_csv

router = APIRouter()
df = read_csv('data/pokemon.csv')

def search_pokemon_info(pokedex_row: Series):
    pokemon = {}

    pokemon['id'] = int(pokedex_row['id'])
    pokemon['species_id'] = pokedex_row['species_id']
    pokemon['name'] = pokedex_row['identifier']
    pokemon['color'] = pokedex_row['color']

    pokemon['types'] = [pokedex_row['type_1']]

    if pokedex_row['type_2'] not in pokemon['types']:
        pokemon['types'].append(pokedex_row['type_2'])

    return pokemon

@router.get('/pokedex/pokemon/name/{pokemon_name}')
async def router_pokemon_name(pokemon_name: str):
    pokemons_series = df[df['identifier'].str.contains(pokemon_name)]
    pokedex = [search_pokemon_info(row) for _, row in pokemons_series.iterrows()]
    return pokedex


@router.get('/pokedex/pokemon/id/{pokemon_id}')
async def router_pokemon_id(pokemon_id: int):
    pokedex_row = [row for _, row in df[df['id'] == pokemon_id].iterrows()][0]
    pokemon = search_pokemon_info(pokedex_row)

    pokemon['hp'] = int(pokedex_row['hp'])
    pokemon['atk'] = int(pokedex_row['atk'])
    pokemon['def'] = int(pokedex_row['def'])
    pokemon['spatk'] = int(pokedex_row['spatk'])
    pokemon['spdef'] = int(pokedex_row['spdef'])
    pokemon['speed'] = int(pokedex_row['speed'])

    # pokemon_info['evolves_from_species_id'] = pokemon_data['evolves_from_species_id']

    return pokemon


@router.get('/pokedex/page/{page}')
async def router_pokemon(page: int):
    i = 30 * page

    pokemons_series = df.iloc[i-30:i]
    pokedex = [search_pokemon_info(row) for _, row in pokemons_series.iterrows()]
    return pokedex