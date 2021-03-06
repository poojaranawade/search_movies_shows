# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 17:37:40 2018

@author: Pooja Ranawade
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os


class items:

    def __init__(self, row):
        self.type = row['titleType']
        self.id = int(row['tconst'])
        self.name = row['primaryTitle']
        self.releaseYear = int(row['startYear'])
        self.ratingLevel = 'Not Adult' if row['isAdult'] == '1' else 'Adult'
        self.genres = row['genres'].split(
            ',') if row['genres'] is not np.nan else []
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

        self.data = pd.read_csv('data/IMDB_new.csv', encoding='cp437')
        self.per_page = 5

    def movie_id(self, id):
        res = self.data.loc[(self.data['tconst'] == int(id)) &
                            (self.data['titleType'].str.contains('movie'))]
        if res.shape[0] == 0:
            response = jsonify(status=422, response={'val': 'id not found'})
            return '', '', response
        else:
            movie = items(res.iloc[0])
            response = jsonify(status=200, response=[movie.serialize()])
            return "movie_id.html", movie, response

    def show_id(self, id):
        res = self.data.loc[(self.data['tconst'] == int(id)) &
                            (self.data['titleType'].str.contains('tv'))]
        if res.shape[0] == 0:
            response = jsonify(status=422, response={'val': 'id not found'})
            return '', '', response
        else:
            show = items(res.iloc[0])
            response = jsonify(status=200, response=[show.serialize()])
            return "show_id.html", show, response

    def search_title(self, title, page):
        if page < 0:
            page = 0
        rows = self.data.loc[
            self.data['primaryTitle'].str.contains(str(title).title())]
        total = rows.shape[0]

        if total == 0:
            response = jsonify(status=422, response={
                               'val': 'similar title not present in dat'})
            return '', '', response

        total_pages = total // self.per_page
        remain = total % self.per_page
        start = ((page - 1) * self.per_page) if page > 1 else 0
        end = start + self.per_page

        print(page, total, total_pages, start, end, remain)
        final = []
        res_list = []
        for index, row in rows.iterrows():
            final.append(items(row))

        if page > total_pages + 1:
            response = jsonify(status=422, response={
                               'val': 'try lower page number'})
            return '', '', response

        elif page == total_pages + 1:
            res_list = jsonify(status=200, response=[
                               e.serialize() for e in final[total_pages * self.per_page:]], page=page,
                               per_page=remain, total_results=total)
            return "search.html", final[total_pages * self.per_page:], res_list

    def search_title_type(self, title, page, type_item):
        if page < 0:
            page = 0
        if type_item == 'show':
            type_item = 'tv'
        rows = self.data.loc[
            (self.data['primaryTitle'].str.contains(str(title).title())) &
            (self.data['titleType'].str.contains(type_item))]
        total = rows.shape[0]

        if total == 0:
            response = jsonify(status=422, response={
                               'val': 'similar title not present in dat'})
            return '', '', response

        total_pages = total // self.per_page
        remain = total % self.per_page
        start = ((page - 1) * self.per_page) if page > 1 else 0
        end = start + self.per_page

        print(page, total, total_pages, start, end, remain)
        final = []
        res_list = []
        for index, row in rows.iterrows():
            final.append(items(row))

        if page > total_pages + 1:
            response = jsonify(status=422, response={
                               'val': 'try lower page number'})
            return '', '', response

        elif page == total_pages + 1:
            res_list = jsonify(status=200, response=[
                               e.serialize() for e in final[total_pages * self.per_page:]], page=page,
                               per_page=remain, total_results=total)
            return "search.html", final[total_pages * self.per_page:], res_list

        res_list = []
        res_list = jsonify(status=200, response=[
                           e.serialize() for e in final[start:end]], page=page,
                           per_page=self.per_page, total_results=total)
        return "search.html", final[start:end], res_list

    def no_page_search_title(self, title):
        rows = self.data.loc[
            self.data['primaryTitle'].str.contains(str(title).title())]
        total = rows.shape[0]

        if total == 0:
            response = jsonify(status=422, response={
                               'val': 'similar title not present in dat'})
            return '', '', response

        final = []
        res_list = []
        for index, row in rows.iterrows():
            final.append(items(row))

        res_list = []
        res_list = jsonify(status=200, response=[
                           e.serialize() for e in final], total_results=total, all_results='yes')
        return "search.html", final, res_list


app = Flask(__name__)
app_obj = Flask_app()


@app.route('/')
def home():
    response = jsonify(status=422, response={
                               'available api': ['/movie/${id}', '/show/${id}', '/search?query={some title}', 
                               '/search?query={some title}&page={some page}']})
    return response


@app.route('/movie/<id>')
def movie_id(id):
    movie_page, movie, response = app_obj.movie_id(id)
    return response


@app.route('/show/<id>')
def show_id(id):
    show_page, show, response = app_obj.show_id(id)
    return response


@app.route('/search')
def search_title():
    title = request.args['query']
    if len(request.args) == 2:
        page = request.args['page']
        search_page, content, response = app_obj.search_title(title, int(page))
    else:
        search_page, content, response = app_obj.no_page_search_title(title)

    if len(request.args) == 3:
        type = request.args['type']
        page = request.args['page']
        search_page, content, response = app_obj.search_title_type(
            title, int(page), type)
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
