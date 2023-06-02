from fastapi import APIRouter
from pandas import Series, read_csv

router = APIRouter()
df = read_csv('data/pokemon.csv')

def search_pokemon_info(pokemon_data: Series):
    pokemon_info = {}

    pokemon_info['id'] = int(pokemon_data['id'])
    pokemon_info['name'] = pokemon_data['identifier']
    pokemon_info['color'] = pokemon_data['color']

    pokemon_info['type_1'] = pokemon_data['type_1']
    pokemon_info['type_2'] = pokemon_data['type_2']

    pokemon_info['hp'] = int(pokemon_data['hp'])
    pokemon_info['atk'] = int(pokemon_data['atk'])
    pokemon_info['def'] = int(pokemon_data['def'])
    pokemon_info['spatk'] = int(pokemon_data['spatk'])
    pokemon_info['spdef'] = int(pokemon_data['spdef'])
    pokemon_info['speed'] = int(pokemon_data['speed'])

    pokemon_info['species_id'] = pokemon_data['species_id']
    pokemon_info['evolves_from_species_id'] = pokemon_data['evolves_from_species_id']

    return pokemon_info


@router.get('/pokemon/name/{pokemon_name}')
async def router_pokemon_name(pokemon_name: str):
    pokemons_df = df[df['identifier'].str.contains(pokemon_name)]
    return [search_pokemon_info(row) for _, row in pokemons_df.iterrows()]


@router.get('/pokemon/id/{pokemon_id}')
async def router_pokemon_id(pokemon_id: int):
    pokemon_series = [row for _, row in df[df['id'] == pokemon_id].iterrows()]
    return search_pokemon_info(pokemon_series[0])


pokedex = [{'id':int(row['id']), 'name': row['identifier']} for _, row in df.iterrows()]

@router.get('/pokemon/')
async def router_pokemon():
    return pokedex