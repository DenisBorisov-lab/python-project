import requests

import models
from database import SessionLocal

token = '784be3af-2393-4535-8562-4cebc84aeeea'

db = SessionLocal()
films = db.query(models.Movie).all()

for film in films:
    r = requests.get('https://kinopoiskapiunofficial.tech/api/v2.2/films', params={
        'keyword': film.name
    }, headers={
        'X-API-KEY': token
    })
    j = r.json()

    if j['total'] == 0:
        print(film.name, 'no image!')
        continue

    item = j['items'][0]
    url = item['posterUrl']

    r = requests.get(url)
    with open()

