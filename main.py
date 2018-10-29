# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 17:37:40 2018

@author: Pooja Ranawade
"""

from flask import Flask, render_template
import pandas as pd


class movies:

    def __init__(self, row):
        self.type = 'movie'
        self.id = row['id']
        self.name = row['movie_title']
        self.releaseYear = int(row['title_year'])
        self.imdb_score = row['imdb_score']
        self.genres = row['genres'].split('|')


class shows:

    def __init__(self, row):
        self.type = 'show'
        self.id = row['id']
        self.name = row['title']
        self.rating = row['rating']
        self.releaseYear = int(row['release_year'])
        self.ratingLevel = row['ratingLevel']


class Flask_app:

    def __init__(self):
        
        def remove_non_ascii(text):
            return ''.join([i if ord(i) < 128 else '' for i in text])
        
        self.movie = pd.read_csv('movie_metadata.csv', encoding='cp437')
        self.shows = pd.read_csv('Netflix_Shows.csv', encoding='cp437')
        self.movie['movie_title'] = self.movie['movie_title'].apply(
            remove_non_ascii)

    def movie_id(self, id):
        row = (self.movie.loc[self.movie['id'] == int(id)].iloc[0])
        return "movie_id.html", movies(row)

    def show_id(self, id):
        row = (self.shows.loc[self.shows['id'] == int(id)].iloc[0])
        return "show_id.html", shows(row)

    def search_title(self, title):
        print(title)
        row_movies = self.movie.loc[self.movie['movie_title'].str.contains(
            'White Chicks')]
        row_shows = self.shows.loc[self.shows['title'].str.contains(
            'White Chicks')]

        final = []
        for index, row in row_movies.iterrows():
            final.append(movies(row))
        for index, row in row_shows.iterrows():
            final.append(shows(row))

        return "search.html", final


app = Flask(__name__)
app_obj = Flask_app()


@app.route('/')
def home():
    return 'home page'


@app.route('/movie/<id>')
def movie_id(id):
    movie_page, movie = app_obj.movie_id(id)
    return render_template(movie_page, movie=movie)


@app.route('/show/<id>')
def show_id(id):
    show_page, show = app_obj.show_id(id)
    return render_template(show_page, show=show)


@app.route('/search/<title>')
def search_title(title):
    search_page, content = app_obj.search_title(title)
    return render_template(search_page, content=content)


if __name__ == '__main__':
    app.run(debug=True)
