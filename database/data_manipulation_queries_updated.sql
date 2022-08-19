--Does the UI utilize a SELECT for every table in the schema? 

--Does at least one SELECT utilize a search/filter with a dynamically populated list of properties?

--Does the UI implement an INSERT for every table in the schema? 
--    In other words, there should be UI input fields that correspond to each table and attribute in that table.

--Does each INSERT also add the corresponding FK attributes, including at least one M:M relationship? 

--Is there at least one DELETE and does at least one DELETE remove things from a M:M relationship? 

--Is there at least one UPDATE for any one entity? 

--Is at least one relationship NULLable? 
    --In other words, there should be at least one optional relationship, e.g. having an Employee might be optional for any Order. Thus it should be feasible to edit an Order and change the value of Employee to be empty.


--------------------------------- MOVIES -----------

--select_all = """
SELECT Movies.movieID, Movies.primaryTitle, Movies.startYear, Genres.genreName
FROM   Movies
JOIN   Genres ON Movies.genreID = Genres.genreID
ORDER BY movieID;

--select_primaryTitle = f"""
SELECT movieID, primaryTitle, startYear, genreName 
FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
WHERE Movies.primaryTitle LIKE %s
ORDER BY movieID --%(title)s;"""
    
    
--select_startYear = f"""
						  SELECT movieID, primaryTitle, startYear, genreName 
						   FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						   WHERE Movies.startYear LIKE %s
						   ORDER BY movieID --%(year)s;"""

--select_title_year = f"""
							SELECT movieID, primaryTitle, startYear, genreName
							FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID
							WHERE Movies.primaryTitle LIKE %(title)s AND Movies.startYear LIKE %s
							ORDER BY movieID--%(year)s;"""

--select_genreName = f"""
							SELECT movieID, primaryTitle, startYear, genreName 
						   FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						   WHERE Movies.genreID = 
						   (SELECT Genres.genreID FROM Genres WHERE Genres.genreName LIKE %s)
						   ORDER BY movieID--%(genre)s);"""

--select_genre_title = f"""
							SELECT movieID, primaryTitle, startYear, genreName 
						   FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						   WHERE Movies.primaryTitle LIKE %(title)s AND Movies.genreID = 
						   (SELECT Genres.genreID FROM Genres WHERE Genres.genreName %s) 
						   ORDER BY movieID--LIKE %(genre)s);"""
						   
--select_genre_title_year = f"""
							SELECT movieID, primaryTitle, startYear, genreName 
						   FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						   WHERE Movies.primaryTitle LIKE %(title)s AND Movies.startYear LIKE %(year)s AND
						   Movies.genreID = (SELECT Genres.genreID FROM Genres WHERE Genres.genreName %s)
						   ORDER BY movieID--LIKE %(genre)s);"""
						   
--select_year_genre = f"""
							SELECT movieID, primaryTitle, startYear, genreName 
						   FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						   WHERE Movies.startYear LIKE %(year)s AND Movies.genreID = 
						   (SELECT Genres.genreID FROM Genres WHERE Genres.genreName LIKE %s)
						   ORDER BY movieID--%(genre)s);"""

--select_title_genre = f"""
						SELECT movieID, primaryTitle, startYear, genreName 
						 FROM Movies JOIN Genres ON Movies.genreID = Genres.genreID 
						 WHERE Movies.primaryTitle LIKE %(title)s AND Movies.genreID = 
						 (SELECT Genres.genreID FROM Genres WHERE Genres.genreName %s) 
						 ORDER BY movieID--LIKE %(genre)s);"""                              



-- get movie to be deleted for showing after delte operation:
--deleted_query = """
SELECT Movies.movieID, Movies.primaryTitle, Movies.startYear, Genres.genreName
   FROM   Movies
   JOIN   Genres ON Movies.genreID = Genres.genreID
   WHERE  movieID = %s; --"""						
--update_movies = """
UPDATE Movies
   SET Movies.primaryTitle = %(title)s,
	   Movies.startYear = %(year)s,
	   Movies.genreID = (SELECT Genres.genreID FROM Genres WHERE Genres.genreName = %(genre)s)
   WHERE
		Movies.movieID = %s -- %(movieID)s;"""
--------------------------------- GENRES -----------

-- populate genre options dropdowns
SELECT Genres.genreName FROM Genres;

-- populate initial Genres table load in webpage
SELECT Genres.genreName, Movies.primaryTitle 
FROM Movies INNER JOIN Genres on Movies.genreID = Genres.genreID
ORDER BY Genres.genreName ASC;

-- search movies by genre (fuzzy search)
SELECT Genres.genreName, Movies.primaryTitle 
FROM Movies INNER JOIN Genres on Movies.genreID = Genres.genreID 
    AND Genres.genreName LIKE (:genreNameInput+%);

-- add new genre
INSERT INTO Genres (genreName) 
VALUES (:genreNameInput);

--------------------------------- ACTORS -----------

-- populate initial Actors_movies table load in webpage
SELECT Actors.primaryName from Actors;

-- search actors
SELECT Actors.primaryName from Actors
WHERE Actors.primaryName LIKE (:actorNameInput+%)

-- add new actor
INSERT INTO Actors (primaryName) 
VALUES (:actorNameInput);

--------------------------------- ACTORS_MOVIES -----------

-- populate initial Actors_movies table load in webpage
SELECT Actors.primaryName, Movies.primaryTitle 
FROM Movies 
INNER JOIN Actors_movies on Movies.movieID = Actors_movies.movieID
INNER JOIN Actors on Actors_movies.actorID = Actors.actorID
ORDER BY Actors.primaryName ASC;

-- search movies by actor (fuzzy search)
SELECT Actors.primaryName, Movies.primaryTitle 
FROM Movies 
INNER JOIN Actors_movies on Movies.movieID = Actors_movies.movieID
INNER JOIN Actors on Actors_movies.actorID = Actors.actorID
    AND Actors.primaryName LIKE (:primaryNameInput+%);

-- add new actor_movie relationship
INSERT INTO Actors_movies (actorID, movieID) 
VALUES (actorID, movieID) (:actorIDInput_from_dropdown, :movieIDInput_from_dropdown);

-- delete actor_movie relationship:
DELETE FROM Actors_movies
WHERE Actors_movies.actorID = :user_specified_actorID_dropdown
    AND Actors_movies.movieID = :user_specified_movieID_dropdown;

--------------------------------- CHARACTERS -----------

-- populate initial Characters table load in webpage
SELECT Characters.characterName, Movies.primaryTitle FROM Movies INNER JOIN Characters on Movies.movieID = Characters.movieID
ORDER BY Characters.characterName ASC;

-- search movies by character (fuzzy search)
SELECT Characters.characterName, Movies.primaryTitle FROM Movies INNER JOIN Characters on Movies.movieID = Characters.movieID
    AND Characters.characterName LIKE (:characterNameInput+%);

-- add new character
INSERT INTO Characters (characterName, actorID, movieID) 
VALUES (:characterNameInput, :actorIDInput, :movieIDInput);


