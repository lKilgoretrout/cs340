import MySQLdb
from flask import Flask, render_template, request, flash
import os

from flask.globals import request
import database.db_connector as db

app = Flask(__name__)
app.secret_key = '$2a$04$9rHv2VcGB.A/t83x.oA5.uIJzEEykE1.VeYX1piO/.uDVctGhlzHO'

# Routes 
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.j2") 

# ----MOVIES routes--------------------------------------------------------------------------------------------
@app.route('/movies', methods=['GET'])
def movies():
    '''display all movies'''    
    db_connection = db.connect_to_database()
    genres_dropdown = get_genres(db_connection)
    
    # no form data --> SELECT *
    select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                    FROM   movies
                    JOIN   genres ON movies.genreID = genres.genreID
                    ORDER BY movies.movieID;"""
    cursor = db.execute_query(db_connection=db_connection, query=select_all)
    movies = cursor.fetchall()
    return render_template("movies.j2", movies=movies, genres=genres_dropdown)
 
# handles the SELECT / SEARCH forms on movies.j2
@app.route('/movies/search', methods=['GET'])
def movies_search():  
    db_connection = db.connect_to_database()
    #if request.form.get('query_type') == 'select':
    primaryTitle = request.args.get('primaryTitle')             
    startYear = request.args.get('startYear')
    genreName = request.args.get('filter_by_genre')
    genres_dropdown = get_genres(db_connection)
    
    populate_genres_dropdown = f"""SELECT genre.genreName FROM genres;"""
    select_primaryTitle = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.primaryTitle LIKE %(title)s
                               ORDER BY movieID;"""
    
    
    select_startYear = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.startYear = %(year)s
                               ORDER BY movieID;"""
    
    select_title_year = f"""SELECT movieID, primaryTitle, startYear, genreName
                                FROM movies JOIN genres ON movies.genreID = genres.genreID
                                WHERE movies.primaryTitle LIKE %(title)s AND movies.startYear = %(year)s
                                ORDER BY movieID;"""
    
    select_genreName = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.genreID = 
                               (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s)
                               ORDER BY movieID;"""
    
    select_genre_title = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.primaryTitle LIKE %(title)s AND movies.genreID = 
                               (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s)
                               ORDER BY movieID;"""
                               
    select_genre_title_year = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.primaryTitle LIKE %(title)s AND movies.startYear = %(year)s AND
                               movies.genreID = (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s)
                               ORDER BY movieID;"""
                               
    select_year_genre = f"""SELECT movieID, primaryTitle, startYear, genreName 
                               FROM movies JOIN genres ON movies.genreID = genres.genreID 
                               WHERE movies.startYear = %(year)s AND movies.genreID = 
                               (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s)
                               ORDER BY movieID;"""
    
    select_title_genre = f"""SELECT movieID, primaryTitle, startYear, genreName 
                             FROM movies JOIN genres ON movies.genreID = genres.genreID 
                             WHERE movies.primaryTitle LIKE %(title)s AND movies.genreID = 
                             (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s) ORDER BY movieID;"""
    
    
    
    # search by startYear only
    if not primaryTitle and \
    startYear and genreName == 'None':
        query = select_startYear
        param = {'year': startYear}
        cursor = db.execute_query(db_connection, query , param) 
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown) 
    
    # search by primarytitle only
    if primaryTitle and not \
    startYear and  genreName == 'None':
        query = select_primaryTitle
        _primaryTitle = '%' + primaryTitle + '%'
        param = {'title': _primaryTitle}
        cursor = db.execute_query(db_connection, query , param)
        print(query)
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)    
        
    # search by genreName only
    if genreName != 'None' and not \
    (startYear or primaryTitle):
            
        query = select_genreName
        #param = (genreName,)
        param = {'genre': genreName}
        cursor = db.execute_query(db_connection, query , param)
        movies = cursor.fetchall()
        
        return render_template("movies.j2", movies=movies, genres=genres_dropdown) 
    
    # search by primaryTItle and startYear
    if startYear and primaryTitle and genreName == 'None':
        query = select_title_year
        primaryTitle = '%' + primaryTitle + '%'
        param = {'title': primaryTitle, 'year': startYear}
        cursor = db.execute_query(db_connection, query , param)
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown) 
    
    
    # search by primaryTitle and genreName
    if primaryTitle and not \
    startYear and genreName != 'None':
            
        query = select_title_genre
        primaryTitle = '%' + primaryTitle + '%'
        param = {'title': primaryTitle, 'genre': genreName}
        cursor = db.execute_query(db_connection, query , param) 
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)
        
    # search by startYear and genreName
    if startYear and not primaryTitle and \
    genreName != 'None':
        query = select_year_genre
        param = {'year': startYear , 'genre': genreName}
        cursor = db.execute_query(db_connection, query , param) 
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)
        
    # search by startYear and genreName AND primaryTitle
    if startYear and primaryTitle and \
    genreName != 'None':
        query = select_genre_title_year
        primaryTitle = '%' + primaryTitle + '%'
        param = {'title': primaryTitle, 'year': startYear , 'genre':genreName}
        cursor = db.execute_query(db_connection, query , param) 
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)
    
    # No search terms used, form submitted anyway:
    if not (primaryTitle and startYear and genreName):
        return render_template("movies.j2", movies=None, genres=genres_dropdown)
 


# handles the UPDATE forms on movies.j2
@app.route('/movies/update', methods=['GET', 'POST'])
def movies_update(): 
    db_connection = db.connect_to_database()
    genres_dropdown = get_genres(db_connection)
    
    if request.method == 'GET':
        
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies , genres=genres_dropdown)
        
    elif request.method == 'POST':
        movieID =          request.form.get('movieID')
        updatedTitle =     request.form.get('updatedTitle')
        updatedStartYear = request.form.get('updatedStartYear')
        updatedGenre =     request.form.get('updatedGenre')
        
        # get and show title of movie that was updated ( the old value to be updated)
        get_title_info = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                            FROM   movies
                            JOIN   genres ON movies.genreID = genres.genreID
                            WHERE  movies.movieID = %s;"""
        parameter = (movieID,)
        cursor = db.execute_query(db_connection, get_title_info, parameter)
        updated_title_data = cursor.fetchone()
        print(updated_title_data)
        
        update_movies = """UPDATE movies
                           SET movies.primaryTitle = %(title)s,
                               movies.startYear = %(year)s,
                               movies.genreID = (SELECT genres.genreID FROM genres WHERE genres.genreName = %(genre)s)
                           WHERE
                                movies.movieID = %(movieID)s;"""
                                
        param = {'title': updatedTitle, 'movieID': movieID, 'year': updatedStartYear, 'genre': updatedGenre}
        cursor = db.execute_query(db_connection, update_movies , param) 
        #cursor.close()
        
        
        
        # show the updated movies again
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        movies = cursor.fetchall()
        
        return render_template("movies.j2" , updated_title_data=updated_title_data, movies=movies, genres=genres_dropdown)
    
    
# handles the INSERT/ADD forms on movies.j2
@app.route('/movies/add', methods=['GET', 'POST'])
def movies_insert():
    '''add a movie to the database'''
    db_connection = db.connect_to_database()
    # populate the dropdown field for selecting a genre with current db values:
    genres_dropdown = get_genres(db_connection)
    
    if request.method == 'GET':
        
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)
        
    elif request.method == 'POST':
        addTitle =     request.form.get('addTitle')
        addStartYear = request.form.get('addStartYear')
        addGenre =     request.form.get('addGenre')
       
       # genre has to be genreID:
        get_genreID = "SELECT genreID FROM genres WHERE genreName = %s;"
        param = (addGenre,)
        cursor = db.execute_query(db_connection=db_connection, query=get_genreID, query_params=param)
        addGenreID = cursor.fetchone()['genreID']    # fetchone() returns: {'genreID': 1}
        print(addGenreID)
        
        
        insert_title = """INSERT INTO movies (primaryTitle, startYear, genreID)
                          VALUES (%(title)s, %(year)s, %(genre)s);"""
        parameters = {'title': addTitle, 'year': addStartYear, 'genre': addGenreID}
        
        
       
        # catch duplicate adds with error flash, flash success if add was successful
        try:
            cursor = db.execute_query(db_connection=db_connection, query=insert_title, query_params=parameters)     
            flash('Successful add!!', 'success')
             
            # ask database what was just added :
            added_movie = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                              FROM movies
                              JOIN genres ON movies.genreID = genres.genreID
                              WHERE primaryTitle = %(title)s AND startYear=%(year)s;"""
            params = {'title': addTitle, 'year': addStartYear}
            cursor = db.execute_query(db_connection=db_connection, query=added_movie, query_params=params)
            added = cursor.fetchone()
        except MySQLdb.IntegrityError:
            flash(f'"{addTitle}"' + ' is already in database ! YOU CAN\'T DO THAT', 'error')
            added = None    
        
        
        # update the movies table with another call to the database
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        movies = cursor.fetchall()
        
        return render_template("movies.j2" , movies=movies, added=added, genres=genres_dropdown)
    
# handles the DELETE forms on movies.j2
@app.route('/movies/delete', methods=['GET', 'POST'])
def movies_delete():
    '''add a movie to the database'''
    db_connection = db.connect_to_database()
    # populate the dropdown field for selecting a genre with current db values:
    genres_dropdown = get_genres(db_connection)
    
    if request.method == 'GET':
        
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        
        movies = cursor.fetchall()
        return render_template("movies.j2", movies=movies, genres=genres_dropdown)
        
    elif request.method == 'POST':
        deleteID =  request.form.get('movieID')
        
        # get movie to be deleted for showing after delte operation:
        deleted_query = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                           FROM   movies
                           JOIN   genres ON movies.genreID = genres.genreID
                           WHERE  movieID = %s;"""
        param = (deleteID,)
        cursor = db.execute_query(db_connection=db_connection, query=deleted_query, query_params=param)
        deleted_movie = cursor.fetchone()
       
        # delete from database using movieID
        delete_by_id = """DELETE FROM movies
                          WHERE movieID = %s;"""
        
        cursor = db.execute_query(db_connection=db_connection, query=delete_by_id, query_params=param)
    
        # show the updated movies again
        select_all = """SELECT movies.movieID, movies.primaryTitle, movies.startYear, genres.genreName
                        FROM   movies
                        JOIN   genres ON movies.genreID = genres.genreID
                        ORDER BY movieID;"""
        cursor = db.execute_query(db_connection=db_connection, query=select_all)
        movies = cursor.fetchall()
        
        return render_template("movies.j2" , movies=movies, deleted_movie=deleted_movie, genres=genres_dropdown)    
    

# ----OTHER routes--------------------------------------------------------------------------------------------

@app.route('/actors', methods=['GET', 'POST'])
def actors():
    db_connection = db.connect_to_database()

    # populate inital table with all actors
    actor_query = "SELECT actors.primaryName FROM actors ORDER BY actors.actorID ASC;"  # doesn't use global function query - different order
    actor_result = db.execute_query(db_connection, actor_query).fetchall()
    
    if request.method == 'POST':
        if 'newName' in request.form:  # insert query
            actor_name = request.form["newName"] 
            query = 'INSERT INTO actors (primaryName) VALUES (%s)'
            db.execute_query(db_connection, query, [actor_name])
            actor_result = db.execute_query(db_connection, actor_query).fetchall()  # refresh table with new actor
            flash(actor_name + ' has been added to the database!', 'success')  # trigger flash message

        else:  # filter by select query
            actor_input = "%" + request.form["primaryName"] + "%"  # allows fuzzy SELECT query

            # override initial actor query
            actor_query = "SELECT actors.primaryName FROM actors WHERE actors.primaryName LIKE (%s);"
            actor_result = db.execute_query(db_connection, actor_query, [actor_input]).fetchall()

    return render_template("actors.j2", values=actor_result) 


@app.route('/genres', methods=['GET', 'POST'])
def genres():
    db_connection = db.connect_to_database()
    
    # populate inital table with all genres and movies
    movie_query = "SELECT genres.genreName, movies.primaryTitle FROM movies INNER JOIN genres on movies.genreID = genres.genreID ORDER BY genres.genreName ASC;"
    movie_result = db.execute_query(db_connection, movie_query).fetchall()

    # query to populate drop-down values and initial table
    """
    genre_query = "SELECT genres.genreName FROM genres ORDER BY genres.genreID;"  # does not use global function - different ordering
    genre_result = db.execute_query(db_connection, genre_query).fetchall()
    """
    genre_result = get_genres(db_connection)

    if request.method == 'POST':
        if "genreName" in request.form:  # insert query
            try:  # attempt insertion, catch errors for duplicate entries
                genre_name = request.form["genreName"]
                query = 'INSERT INTO genres (genreName) VALUES (%s)'
                db.execute_query(db_connection, query, [genre_name])
            except MySQLdb.IntegrityError:
                flash(genre_name + ' is already in the database! Please try a different option.', 'error')
            else:
                flash(genre_name + ' has been added to the database!', 'success')  # trigger flash message
                genre_result = get_genres(db_connection)  # refresh dropdown list with new genre

        else:  # filter by select query
            genre_input = request.form["search_by_genre"]

            # override initial genre query
            movie_query ="SELECT genres.genreName, movies.primaryTitle FROM movies INNER JOIN genres on movies.genreID = genres.genreID AND genres.genreName = %s;"
            movie_result = db.execute_query(db_connection, movie_query, [genre_input]).fetchall()

    return render_template("genres.j2", values=movie_result, genres=genre_result)


@app.route('/characters', methods=['GET', 'POST'])
def characters():
    db_connection = db.connect_to_database()

    # populate initial table with all characters
    character_query = "SELECT characters.characterName FROM characters ORDER BY characters.characterID;"
    character_result = db.execute_query(db_connection, character_query).fetchall()

    # populate inital table with all characters and their movies
    character_movie_query = "SELECT characters.characterName, movies.primaryTitle FROM movies INNER JOIN characters on movies.movieID = characters.movieID ORDER BY characters.characterName ASC;"
    character_movie_result = db.execute_query(db_connection, character_movie_query).fetchall()

    # query to populate drop-down values
    actor_query_results = actor_query(db_connection)
    movie_query_results = movie_query(db_connection)

    if request.method == 'POST':
        if "primaryName" in request.form:  # insert query
            character_name = request.form["characterName"]
            actor_name = request.form["primaryName"]
            actor_id = db.execute_query(db_connection, "SELECT actors.actorID from actors WHERE actors.primaryName =%s;", [actor_name]).fetchone()
            movie_name = request.form["primaryTitle"]
            movie_id = db.execute_query(db_connection, "SELECT movies.movieID from movies WHERE movies.primaryTitle =%s;", [movie_name]).fetchone()
            query = "INSERT INTO characters (characterName, actorID, movieID) VALUES (%s, %s, %s);"

            try:  # attempt insertion, catch errors for duplicate entries
                db.execute_query(db_connection, query, [character_name, actor_id['actorID'], movie_id['movieID']])
            except MySQLdb.IntegrityError:
                flash(character_name + ' is already in the database! Please try a different option.', 'error')
            else:
                character_movie_result = db.execute_query(db_connection, character_movie_query).fetchall()  # refresh table with new character
                flash(character_name + ' has been added to the database!', 'success')  # trigger flash message

        else:  # filter by select query
            character_input = "%" +  request.form["characterName"] + "%"  # allows fuzzy SELECT query

            # override initial character/movie query
            character_movie_query = "SELECT characters.characterName, movies.primaryTitle FROM movies INNER JOIN characters on movies.movieID = characters.movieID AND characters.characterName LIKE (%s);"
            character_movie_result = db.execute_query(db_connection, character_movie_query, [character_input]).fetchall()
    
    return render_template("characters.j2", characters=character_result, values=character_movie_result, actors=actor_query_results, movies=movie_query_results)

@app.route('/actors_movies', methods=['GET', 'POST'])
def actors_movies():
    db_connection = db.connect_to_database()

    # populate inital table with all genres
    actor_movie_query = "SELECT actors.primaryName, movies.primaryTitle FROM movies INNER JOIN actors_movies on movies.movieID = actors_movies.movieID INNER JOIN actors on actors_movies.actorID = actors.actorID ORDER BY actors.primaryName ASC;"
    actor_movie_result = db.execute_query(db_connection, actor_movie_query).fetchall()

    if request.method == 'POST':
        if "select_movie" in request.form:  # insert or delete query
            movie_input = request.form["select_movie"]
            movie_id = db.execute_query(db_connection, "SELECT movies.movieID from movies WHERE movies.primaryTitle =%s;", [movie_input]).fetchone()
            actor_input = request.form["select_actor"]
            actor_id = db.execute_query(db_connection, "SELECT actors.actorID from actors WHERE actors.primaryName =%s;", [actor_input]).fetchone()
            
            #return request.form["Name"]
            
            # logic to handle INSERT OR DELETE by different submission buttons
            if request.form["submit"] == "ADD PAIR":
                query = "INSERT INTO actors_movies (actorID, movieID) VALUES (%s, %s);"
            elif request.form["submit"] == "DELETE PAIR":
                query = "DELETE FROM actors_movies WHERE actors_movies.actorID = %s AND actors_movies.movieID = %s;"

            try:  # attempt insertion, catch errors for duplicate entries
                db.execute_query(db_connection, query, [actor_id['actorID'], movie_id['movieID']])
            except MySQLdb.IntegrityError:
                flash('Pair: ' + movie_input + '/' + actor_input + ' is already in the database! Please try a different option.', 'error')
            else:
                actor_movie_result = db.execute_query(db_connection, actor_movie_query).fetchall()  # refresh table with new actor/movie pair
                flash('Pair: ' + movie_input + '/' + actor_input + ' has been added to the database!', 'success') # trigger flash message
        else: # filter by select query
            actor_input = "%" + request.form["primaryName"] + "%"  # allows fuzzy SELECT query

            # override initial actor query
            actor_movie_query = "SELECT actors.primaryName, movies.primaryTitle FROM movies INNER JOIN actors_movies on movies.movieID = actors_movies.movieID INNER JOIN actors on actors_movies.actorID = actors.actorID AND actors.primaryName LIKE (%s);"
            actor_movie_result = db.execute_query(db_connection, actor_movie_query, [actor_input]).fetchall()


    # query to populate drop-down values
    actor_query_results = actor_query(db_connection)
    movie_query_results = movie_query(db_connection)


    return render_template("actors_movies.j2", values=actor_movie_result, actors=actor_query_results, movies=movie_query_results)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.j2'), 404

# commonly used queries ----------------------------------------------------------------------------------------------------
def actor_query(database_connection) -> list:
    actor_query = "SELECT actors.primaryName FROM actors ORDER BY actors.primaryName ASC;"
    return db.execute_query(database_connection, actor_query).fetchall()

def movie_query(database_connection) -> list:
    movie_query = "SELECT movies.primaryTitle FROM movies ORDER BY movies.primaryTitle ASC;"
    return db.execute_query(database_connection, movie_query).fetchall()

def get_genres(database_connection):
    # populate the dropdown field for selecting a genre with current db values:
    genres_dropdown = f"""SELECT genres.genreName FROM genres ORDER BY genres.genreName;"""
    query = genres_dropdown
    cursor = db.execute_query(database_connection, query)
    genres = cursor.fetchall()
    return genres


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 42420)) 
    app.run(port=port, debug=True)
