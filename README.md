# Search for Movies and Shows
Search for Movies and shows using API written in Python

# Design a REST API with three endpoints:

1. **/movie/${id}**
  - when given the appropriate id, will yield the movie matching that identifier (more on where that id comes from shortly).
2. **/show/${id}** 
  - when given the appropriate id, will yield the show matching that identifier.
3. The 1,2 endpoints should contain, at minimum, the title, release year, and a synopsis of the media item being displayed.
4. **/search/${some title}** 
  - when given a '?query=${some title}', will yield any movies or shows matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show.
5. **/search/${some title}/page/${int: page number}** 
   - when given a '?query=${some title}', will yield _paginated_ any movies or shows matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show.


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


# How to use
**to use locally**
- open terminal and cd to the directory where all these files are saved
- Run
  - to see json response on browser: python main_json_response.py
  - to see html pages: python main_html_render.py
- open browser and go to 
  - **/movie/${id}** : http://localhost:5000/movie/9
  - **/show/${id}** : http://localhost:5000/show/29270
  - **/search/${some title}** : http://localhost:5000/search/merry
  - **/search/${some title}/page/${int: page number}** : http://localhost:5000/search/merry/page/25
