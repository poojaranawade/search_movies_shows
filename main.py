# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 17:37:40 2018

@author: Pooja Ranawade
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np


class items:

    def __init__(self, row):
        self.type = row['titleType']
        self.id = int(row['tconst'])
        self.name = row['primaryTitle']
        self.releaseYear = int(row['startYear'])
        self.ratingLevel = True if row['isAdult'] == '1' else False
        self.genres = row['genres'].split(',')
        self.time = str(row['runtimeMinutes']) + ' minutes'

    def serialize(self):
        return {'name': self.name,
                'type': self.type,
                'id': self.id,
                'releaseYear': self.releaseYear,
                'ratingLevel': self.ratingLevel,
                'genres': self.genres,
                'time': self.time}


class Flask_app:

    def __init__(self):

        def remove_non_ascii(text):
            return ''.join([i if ord(i) < 128 else '' for i in text])

        self.data = pd.read_csv('IMDB.csv', encoding='cp437')
        self.per_page = 2

        # remove empty, null, nan
        self.data['titleType'].replace('', np.nan, inplace=True)
        self.data.dropna(subset=['titleType'], inplace=True)
        self.data['primaryTitle'].replace('', np.nan, inplace=True)
        self.data.dropna(subset=['primaryTitle'], inplace=True)
        headers = list(self.data.columns.values)

    def movie_id(self, id):
        res = self.data.loc[(self.data['tconst'] == int(id)) &
                            (self.data['titleType'].str.contains('movie'))]
        if res.shape[0] == 0:
            response = jsonify(status=404, response={'val': 'not found'})
            return '', '', response
        else:
            movie = items(res.iloc[0])
            response = jsonify(status=200, response=[movie.serialize()])
            return "movie_id.html", movie, response

    def show_id(self, id):
        res = self.data.loc[(self.data['tconst'] == int(id)) &
                            (self.data['titleType'].str.contains('tv'))]
        if res.shape[0] == 0:
            response = jsonify(status=404, response={'val': 'not found'})
            return '', '', response
        else:
            show = items(res.iloc[0])
            response = jsonify(status=200, response=[show.serialize()])
            return "show_id.html", show, response

    def search_title(self, title, page):
        if page < 0:
            page = 0
        rows = self.data.loc[self.data['primaryTitle'].str.contains(str(title))]

        if rows.shape[0] == 0:
            response = jsonify(status=404, response={'val': 'not found'})
            return '', '', response

        final = []
        res_list = []
        for index, row in rows.iterrows():
            final.append(items(row))

        print(len(final), page, self.per_page, final)
        if len(final) < (page + self.per_page - 1):
            response = jsonify(status=404, response={'val': 'try lower page'})
            return '', '', response
        else:
            res_list = jsonify(status=200, response=[
                               e.serialize() for e in final[page:page + self.per_page]])
            return "search.html", final[page:page + self.per_page], res_list


app = Flask(__name__)
app_obj = Flask_app()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/movie/<id>')
def movie_id(id):
    movie_page, movie, response = app_obj.movie_id(id)
#    return render_template(movie_page, movie=movie)
    return response


@app.route('/show/<id>')
def show_id(id):
    show_page, show, response = app_obj.show_id(id)
#    return render_template(show_page, show=show)
    return response


@app.route('/search/<title>/page/<page>')
def search_title(title, page=1):
    search_page, content, response = app_obj.search_title(title, int(page) - 1)
#    return render_template(search_page, content=content)
    return response


if __name__ == '__main__':
    app.run(debug=True)
