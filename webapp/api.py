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


@api.route('/results/<song_search>')
def get_results(song_search):

    modified_search = "'%%" + song_search + "%%'"
    print(modified_search)

    query = '''SELECT song_id, name, artist, highest_pos, streams
      FROM songs
      WHERE UPPER(name) LIKE UPPER(''' + modified_search + ''')
      ORDER BY name;'''

    print(query)

    song_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (song_search))
        for row in cursor:
            song = {'id':row[0],'name':row[1],'artist':row[2],'highest_pos':row[3],'streams':row[4]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)

@api.route('/songs-like/<song_search>')
def get_songs_like(song_search):

    modified_search = "'%%" + song_search + "%%'"
    print(modified_search)

    query_1 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
      FROM songs, attributes
      WHERE UPPER(name) = UPPER(''' + modified_search + ''') AND song_id = attributes_id;'''

    query_2 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
      FROM songs, attributes
      WHERE song_id = attributes_id;'''

    print(query_1)

    song_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (song_search))
        for row in cursor:
            found_song = {'id':row[0],'name':row[1],'artist':row[2], 'dancaeability':row[4], 'energy':row[5], 'loudness':row[6], 'speechiness':row[7], 'acousticness':row[8], 'liveness':row[9], 'tempo':row[10], 'duration':row[11], 'valence':row[12]}
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (song_search))
        for row in cursor:
            if row[0] != found_song['id']:
                likeness = (1-abs(found_song['dancaeability']-row[4]))+(1-abs(found_song['energy']-row[5]))+(26.8-abs(found_song['loudness']-row[6]))/30+(1-abs(found_song['speechiness']-row[7]))+(1-abs(found_song['acousticness']-row[8]))/2+(1-abs(found_song['liveness']-row[9]))/3+(160-abs(found_song['tempo']-row[10]))/640+(558000-abs(found_song['duration']-row[11]))/3348000+(1-abs(found_song['valence']-row[12]))/10
                song = {'id':row[0],'name':row[1],'artist':row[2],'likeness':likeness}
                song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    def myFunc(e):
        return e['likeness']

    song_list.sort(key=myFunc)

    return json.dumps(song_list[0:20])
