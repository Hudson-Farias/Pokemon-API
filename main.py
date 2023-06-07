from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from importlib import import_module
from os import listdir

app = FastAPI(docs_url = '/')

origins = [
    'http://pokenext-shinikatame.vercel.app',
    'https://pokenext-shinikatame.vercel.app',

    'http://pokenext-git-main-shinikatame.vercel.app',
    'https://pokenext-git-main-shinikatame.vercel.app',

    'http://pokenext-sigma-eight.vercel.app',
    'https://pokenext-sigma-eight.vercel.app',

    'http://pokenext-6if1aljh5-shinikatame.vercel.app',
    'https://pokenext-6if1aljh5-shinikatame.vercel.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['GET'],
    allow_headers = ['*']
)

def load(path = 'routers'): 
    for file in listdir(path):
        if file not in ['__pycache__', '__init__.py']:
            if file.endswith('.py'):
                module = import_module(f'{path}.{file}'.replace('.py', ''))
                app.include_router(module.router)

            else:
                load(path + '/' + file)

load()

if __name__ == '__main__': 
    run(app)