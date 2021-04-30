
# -*- coding: utf-8 -*-
'''
MARVEL'S API
La API de Marvel Comics es una herramienta para ayudar a los desarrolladores de 
todo el mundo a crear sitios web y aplicaciones asombrosos, asombrosos e increíbles 
utilizando datos de los más de 70 años de la era de los cómics Marvel.

fuente: "http://marvel.com\">Data provided by Marvel. © 2021 MARVEL

'''

__author__ = 'eddie75espinoza'
__date__ = '24/04/2021'


from flask import Flask, request, render_template, jsonify, url_for
from secureconfig import PRIVATE_API_KEY, PUBLIC_API_KEY
import pymarvel
import requests

app = Flask(__name__)

VERSION_DEFAULT = 'v1' # por si es requerida una actualización de versión
public = PUBLIC_API_KEY
private = PRIVATE_API_KEY

base = 'https://gateway.marvel.com/%s/public/' %(VERSION_DEFAULT)

# -------- ROUTES ---------------------

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        hero_list = pymarvel.character_general() 
        if request.method == 'POST':
            # se usa este metodo para obtener el valor del form
            name = request.form['name']
            return hero(name)
    except NameError:
        print('Page not found... 404')

    return render_template('marvel/home.html', hero_list = hero_list)

@app.route('/heroes', methods=['GET', 'POST'])
def heroes():
#obtiene un listado de 100 (api limit) heroes
    try:
        hero_list = pymarvel.character_general() 
        if request.method == 'POST':
            # se usa este metodo para obtener valor del form
            name = request.form['name']
            return hero(name)

    except IndexError:
        print('Error...404')
    return render_template('marvel/heroes.html', hero_list = hero_list)

@app.route('/hero/<name>', methods=['GET', 'POST'])
def hero(name):
# valores individuales de un personaje, incluye comics y series por id de personaje
    try: 

        hero_list = pymarvel.character_general(name)[0] 
        id = hero_list.get('id')            
        comic_hero_list = pymarvel.get_comics_by_characterId(id)                 
        serie_character = pymarvel.get_serie_by_id_character(id)

    except IndexError:
        print("Something else went wrong...404")        
        return render_template('marvel/404.html')
    return render_template('marvel/hero.html', hero_list = hero_list, comic_hero_list= comic_hero_list,serie_character = serie_character)  

@app.route('/series', methods=['GET', 'POST'])
def series_startName():
    series_list = pymarvel.get_series_by_startName('avengers').get('data').get('results')
         
    return render_template('marvel/seriescomics.html', data_list = series_list)

@app.route('/comics')
def comics():
    comics_list = pymarvel.comics('spider-man').get('data').get('results')  

    return render_template('marvel/seriescomics.html', data_list = comics_list)

@app.route('/about')
def about():
    
    return render_template('marvel/about.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 4000, debug=True)