'''
    api.py
    Aaron Schondorf and Jared Chen, 11 November 2021

'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/load-genres')
def load_genres():
    '''Loads all genres from database and returns it in json formate. used to populate
    The drop down genre search.'''

    query = '''  SELECT DISTINCT genre
        FROM genres
        ORDER BY genre;'''

    genre_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            genre = {'genre':row[0]}
            genre_list.append(genre)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(genre_list)



@api.route('/results')
def get_results():
    '''This function takes in all potential parameters given by user and returns a
    json formate dictionary of all songs that match those parameters.'''

    song_search = flask.request.args.get('song')
    artist_search = flask.request.args.get('artist')
    genres = flask.request.args.get('genres')
    sort_by = flask.request.args.get('key')
    sort_order = flask.request.args.get('order')
    string_song_search = str(song_search)
    string_artist = str(artist_search)
    string_genres = str(genres)
    string_sort_by = str(sort_by)
    string_sort_order = str(sort_order)

    #set default values for sorting in sql query
    if sort_by is None:
        string_sort_by = 'UPPER(name)'
    elif string_sort_by == 'artist' or string_sort_by == 'name' or string_sort_by == 'genres_list':
        string_sort_by = 'UPPER(' + string_sort_by + ')'

    if sort_order is None:
        string_sort_order = 'ASC'

    #Modifying search string so they can be added to sql query
    modified_song = "'%%" + string_song_search + "%%'"
    modified_artist = "'%%" + string_artist + "%%'"
    genre_sql_code = ''
    genre_list = string_genres.split(",")

    #parses genre_list so all genres can be searcehd for.
    for item in genre_list:
        if genre_sql_code == '' and item != '':
            genre_sql_code += "AND (genre = '" + item + "') "
        elif len(genre_list) > 1:
            genre_sql_code += "OR (genre = '" + item + "')"

    query = '''SELECT DISTINCT song_id, name, artist, highest_pos, streams, genres_list, UPPER(name),
     UPPER(artist), UPPER(genres_list)
      FROM songs
      JOIN genres
      ON song_id = genre_id
      WHERE UPPER(name) LIKE UPPER(''' + modified_song + ''')
      AND UPPER(artist) LIKE UPPER(''' + modified_artist + ''')
      ''' + genre_sql_code + '''
      ORDER BY ''' + string_sort_by +''' ''' + string_sort_order + ''';'''

    song_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            song = {'id':row[0],'name':row[1],'artist':row[2],'highest_pos':row[3],'streams':row[4]
            , 'genres_list' : row[5]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)

@api.route('/songs-like/<song_search>')
def get_songs_like(song_search):
    '''This returns a json formatted dictionary of 20 songs with the highest likeness score.'''
    sort_by = flask.request.args.get('key')
    sort_order = flask.request.args.get('order')
    string_sort_by = str(sort_by)
    string_sort_order = str(sort_order)
    boolean_sort_order = True

    if sort_by is None:
        string_sort_by = 'likeness'
    if sort_order is None:
        string_sort_order = 'DESC'
    if string_sort_order == 'ASC':
        boolean_sort_order = False
    if string_sort_by == 'likeness' and sort_by is None:
        boolean_sort_order = True


    modified_song = "'%%" + song_search + "%%'"

    query_1 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence, genres_list
      FROM songs, attributes
      WHERE UPPER(name) LIKE UPPER(''' + modified_song + ''') AND song_id = attributes_id;'''

    query_2 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence, genres_list
      FROM songs, attributes
      WHERE song_id = attributes_id;'''

    song_list = []

    #Instantiate song that is being searched for in both raw and formatted form
    found_song = {'id':0,'name':'none','artist':'none', 'genres_list':'none', 'dancaeability':0.0, 'energy':0.0,
     'loudness':0.0, 'speechiness':0.0, 'acousticness':0.0, 'liveness':0.0, 'tempo':0.0, 'duration':0.0, 'valence':0.0}
    formatted_found_song = song = {'id':0,'name':'none','artist':'none', 'genres_list':'none', 'likeness':10}

    #Query to find the search song
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query_1)
        row = cursor.fetchone()
        found_song = {'id':row[0],'name':row[1],'artist':row[2], 'genres_list':row[13], 'dancaeability':row[4],
         'energy':row[5], 'loudness':row[6], 'speechiness':row[7], 'acousticness':row[8], 'liveness':row[9],
         'tempo':row[10], 'duration':row[11], 'valence':row[12]}
        formatted_found_song = {'id':row[0],'name':row[1],'artist':row[2], 'genres_list':row[13], 'likeness':10}
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    #Looping through all songs to generate the likeness score that is a comparison between each song and the song queried above
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query_2)
        for row in cursor:
            if row[0] != found_song['id']:
                likeness = (1.0-abs(float(found_song['dancaeability'])-float(row[4])))+(1.0-abs(float(found_song['energy'])
                -float(row[5])))+(26.8-abs(float(found_song['loudness'])-float(row[6])))/30+(1.0-abs(float(found_song['speechiness'])
                -float(row[7])))+(1.0-abs(float(found_song['acousticness'])-float(row[8])))/2+(1.0-abs(float(found_song['liveness'])
                -float(row[9])))/3+(160.0-abs(float(found_song['tempo'])-float(row[10])))/640+(558000.0-abs(float(found_song['duration'])
                -float(row[11])))/3348000+(1.0-abs(float(found_song['valence'])-float(row[12])))/10
                song = {'id':row[0],'name':row[1],'artist':row[2], 'genres_list': row[13], 'likeness':round(likeness,4)}
                song_list.append(song)

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    #first_sort sorts all results based on likeness score.
    def first_sort(e):
        return e['likeness']
    #second_sort sorts all results based on user specified variable
    def second_sort(e):
        return e[string_sort_by]

    #Sort by likeness and slice to get the 20 most similar songs
    song_list.sort(reverse=True, key=first_sort)
    song_list = song_list[0:20]
    #Sort based on user's input
    song_list.sort(reverse = boolean_sort_order, key=second_sort)

    #Add original song to beginning of the list so we can display it
    song_list.insert(0, formatted_found_song)

    return json.dumps(song_list)

#api/help enpoint documentation
@api.route('/help')
def get_help():
    return flask.render_template('help.html')
