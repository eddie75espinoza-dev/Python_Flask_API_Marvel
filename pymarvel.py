from datetime import datetime
from secureconfig import PRIVATE_API_KEY, PUBLIC_API_KEY
from model import Heroe
import json
import hashlib
import requests


VERSION_DEFAULT = 'v1' # por si es requerida una actualización de versión
public = PUBLIC_API_KEY
private = PRIVATE_API_KEY

base = 'https://gateway.marvel.com/%s/public/' %(VERSION_DEFAULT)

now = datetime.now()
ts = str(int(datetime.timestamp(now))) # ts = timestamp
_hash = hashlib.md5((ts + private + public).encode()).hexdigest()

def character_general(*arg):
    ''' :param = name (of Hero)
    Obtiene el nombre y caracteristicas generales de el personaje
    '''
    by_name = requests.get(base + 'characters',
                          params={'apikey': public,
                                  'ts': ts,
                                  'hash': _hash,                                  
                                  'nameStartsWith': arg,
                                  'limit': 100}).json()
    data = by_name.get('data').get('results')   
    return data

def get_series_by_startName(*arg):
    ''' :param = name (of Serie)
    Obtiene las caracteristicas generales de una serie
    toma como argumento el nombre con el que inicia la
    serie
    '''
    data_series = requests.get(base + 'series',
                          params={'apikey': public,
                                  'ts': ts,
                                  'hash': _hash,
                                  'titleStartsWith': arg,
                                  'limit': 52}).json()
     
    return data_series

def comics(*arg):
    list_comics = requests.get(base + 'comics',params={
                                'apikey': public,
                                'ts': ts,
                                'hash': _hash,
                                'title': arg}).json()
    return list_comics

def get_comics_by_characterId(id):
    ''' :param = id (of Hero)
    Obtiene las asociadas a el personaje
    '''
    data = requests.get(base + f'characters/{id}/comics?orderBy=-onsaleDate',
                          params={'apikey': public,
                                  'ts': ts,
                                  'hash': _hash}).json() 
    data_comics = data.get('data').get('results')     
    return data_comics

def get_serie_by_id_character(id):
    ''' :param = id (of Hero)
    Obtiene las asociadas a el personaje
    '''
    data = requests.get(base + f'characters/{id}/series',
                          params={'apikey': public,
                                  'ts': ts,
                                  'hash': _hash}).json() 
    data_serie = data.get('data').get('results')     
    return data_serie