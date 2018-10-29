# Search for Movies and Shows
Search for Movies and shows using API written in Python

# Design a REST API with three endpoints:

1. # /movie/${id} 
  when given the appropriate id, will yield the movie matching that identifier (more on where that id comes from shortly).
2. # /show/${id} 
  when given the appropriate id, will yield the show matching that identifier.
3. # /search 
  when given a '?query=${some title}', will yield any movies or shows matching that title, returning a JSON of matching titles, the years the media items were released, and whether each media item is a movie or a show. These results should be paginated.
4. The 1,2 endpoints should contain, at minimum, the title, release year, and a synopsis of the media item being displayed.

# The data
Using Netflix shows and Movie data 
