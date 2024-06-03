import asyncio
import os

import aiofiles
import aiohttp

import models
from database import SessionLocal

TOKEN = ''
BASE_URL = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'
HEADERS = {'X-API-KEY': TOKEN}
IMAGE_DIR = './images_films'
WORKERS = 4

async_session = SessionLocal


async def fetch_film_data(session, film_name):
    params = {'keyword': film_name}
    async with session.get(BASE_URL, params=params, headers=HEADERS) as response:
        return await response.json()


async def download_image(session, film_name, url):
    image_path = os.path.join(IMAGE_DIR, f'{film_name}.jpg')
    async with session.get(url) as response:
        content = await response.read()
    async with aiofiles.open(image_path, 'wb') as f:
        await f.write(content)


async def process_film(film, session):
    film_name = film.name
    image_path = os.path.join(IMAGE_DIR, f'{film_name}.jpg')

    if os.path.exists(image_path):
        print(f'Skipping {film_name}, already exists!')
        return

    film_data = await fetch_film_data(session, film_name)
    if film_data['total'] == 0:
        print(f'{film_name} has no image!')
        return

    item = film_data['items'][0]
    await download_image(session, film_name, item['posterUrl'])
    print(f'{film_name} done.')


async def worker(name, films):
    async with aiohttp.ClientSession() as aiohttp_session:
        for film in films:
            try:
                await process_film(film, aiohttp_session)
            except:
                print(f'{name}: {film.name} err')

            print(f'{name}: {film.name} processed.')


async def main():
    with async_session() as db:
        films = db.query(models.Movie).all()

    chunk_size = len(films) // WORKERS
    film_chunks = [films[i:i + chunk_size] for i in range(0, len(films), chunk_size)]

    tasks = [worker(f'Worker-{i + 1}', chunk) for i, chunk in enumerate(film_chunks)]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
