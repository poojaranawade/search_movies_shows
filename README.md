# Search for Movies and Shows
Search for Movies and shows using API written in Python

# Design a REST API with three endpoints:

1. **/movie/${id}**
  - when given the appropriate id, will yield the movie matching that identifier (more on where that id comes from shortly).
2. **/show/${id}** 
  - when given the appropriate id, will yield the show matching that identifier.
3. The 1,2 endpoints should contain, at minimum, the title, release year, and a synopsis of the media item being displayed.
4. **/search?query=${some title}** 
  - when given a '?query=${some title}', will yield any movies or shows matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show.
5. **/search?query=${some title}&page=${int: page number}** 
   - when given a '?query=${some title}', will yield _paginated_ any movies or shows matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show.
6. **/search?query=${some title}&page=${int: page number}&type=${'show' or 'movie'}**
  - when given a '?query=${some title}', will yield _paginated_ given type and matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show.


# The data
Using IMDB shows and Movie data can be found at https://www.imdb.com/interfaces/ by title _title.basics.tsv.gz_.
 
**Contains the following information for titles:**
- **tconst (int)** - numeric unique identifier of the title used as ${id}
- **titleType (string)** – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
- **primaryTitle (string)** – the more popular title / the title used by the filmmakers on promotional materials at the point of release
- **originalTitle (string)** - original title, in the original language
- **isAdult (boolean)** - 0: non-adult title; 1: adult title
- **startYear (YYYY)** – represents the release year of a title. In the case of TV Series, it is the series start year
- **endYear (YYYY)** – TV Series end year. blank for all other title types
- **runtimeMinutes** – primary runtime of the title, in minutes
- **genres (string array)** – includes up to three genres associated with the title

# Requirements
Flask==1.0.2
numpy==1.14.3
pandas==0.23.0

# How to use
**to install required libraries**
pip install -r requirements.txt

**to use locally**
- open terminal and cd to the directory where all these files are saved
- Run
  - to see json response on browser: python main_json_response.py
  - to see html pages: python main_html_render.py
- open browser and go to 
  - /movie/${id} : http://localhost:5000/movie/9
  - /show/${id} : http://localhost:5000/show/269988
  - /search?query= ${some title} :  http://localhost:5000/search?query=merry
  - /search?query=${some title}&page=${int: page number} : http://localhost:5000/search?query=merry&page=10  
  - /search?query=${some title}&page=${int: page number}&type=${'show' or 'movie'} : http://localhost:5000/search?query=merry&page=10&type=show

# Deployed on Heroku
**Check Deployed version**
- /movie/${id} : https://search-movies-shows.herokuapp.com/movie/9
- /show/${id} : https://search-movies-shows.herokuapp.com/show/269988
- /search?query= ${some title} :  https://search-movies-shows.herokuapp.com/search?query=merry
- /search?query=${some title}&page=${int: page number} : https://search-movies-shows.herokuapp.com/search?query=merry&page=10
- - /search?query=${some title}&page=${int: page number}&type=${'show' or 'movie'} : https://search-movies-shows.herokuapp.com/search?query=merry&page=10&type=show


**steps to deploy**

Following steps from https://devcenter.heroku.com/articles/getting-started-with-python#set-up
1. Install Heroku Client from https://devcenter.heroku.com/articles/heroku-cli#download-and-install
2. Open cmd after installation is finished, run `heroku login` and enter email address and password
3. go to app directory
4. create requirements file by using `pip freeze > requirements.txt` 
    **dont forget to remove the libraries that are not used in this app**
5. heroku create app-name to create app on heroku e.g. `heroku create search-movies-shows`
**dont forget to create Procfile** Procfile contents `web: python main.py`
6. `git push heroku master` to push changes in the heroku app
7. `heroku ps:scale web=1` to ensure that app is running
8. go to https://search-movies-shows.herokuapp.com/ to see results
