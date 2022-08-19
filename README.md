# cs340
Online Eric Roberts Database

Eric Roberts has starred in 628 movies and a dozen or so new movies each
year. Keeping track of all them
is burden to the casual viewer. IOERD is a scaled down version of the
Internet Movie Database (imdb.com) that
allows the user to search movies with Eric Robert by complete or partial
movie title, the year a movie was produced
the full or partial name of co-stars in that movie or the name of a
character in the movie or by genre.

The MySQL database is organized in the following scheme:

Movies ( each Movies has an id, a title and a startYear (when it was filmed))
tConst INT, AUTO_INCREMENT, UNIQUE, NOT NULL, PRIMARY KEY
primaryTitle VARCHAR
startYear INT
genreConst INT
...
relationship: a M:M relationship between Movies and Actors
a M:1 relationship between Movies and Genres
using FOREIGN KEY (genreConst) REFERENCES Genres (gConst)
Actors
nConst INT, AUTO_INCREMENT, UNIQUE, NOT NULL, PRIMARY KEY
primaryName VARCHAR NOT NULL
...
relationship: M:M relationship between Actors and Movies
1:M relationship between Actors and Characters
Actors_movies (M:M, matches an actor and the movie(s) that they are best known for)
actorMovieID INT, AUTO_INCREMENT, UNIQUE, NOT NULL, PRIMARY KEY
nameConst INT
knownForTitle INT
...
relationship: M:M between Actors and Movies
Using FOREIGN KEY(knownForTitle) that REFERENCES Movies(tConst)
and FOREIGN KEY(nameConst) that REFERENCES Actors(nConst)
Characters (the characters that appear in movies)
characterConst INT AUTO_INCREMENT, NOT NULL, PRIMARY KEY
character VARCHAR
...
relationship: 1:M between Actors and Characters
Actors_characters (bridge table between actors and the roles they play in a
particular movie)
PRIMARY KEY (titleConst,namingConst)
FOREIGN KEY titleConst INT REFERENCES Movies(tConst)
FOREIGN KEY namingConst INT REFERENCES Actors(nConst)
FOREIGN KEY charConst INT REFERENCES Characters(characterConst)
Genres(genres of movies, e.g. action, horror, comedy (each movie only has one
genre))
gConst INT, AUTO_INCREMENT, UNIQUE, NOT NULL, PRIMARY KEY
genreName VARCHAR
...
relationship: 1:M, matching Genres and Movies
