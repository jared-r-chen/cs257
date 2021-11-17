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
    sort_by = flask.request.args.get('key')
    sort_order = flask.request.args.get('order')
    string_sort_by = str(sort_by)
    string_sort_order = str(sort_order)

    if sort_by is None:
        string_sort_by = 'name'
    if sort_order is None:
        string_sort_order = 'ASC'


    modified_search = "'%%" + song_search + "%%'"
    print(modified_search)

    query = '''SELECT song_id, name, artist, highest_pos, streams
      FROM songs
      WHERE UPPER(name) LIKE UPPER(''' + modified_search + ''')
      ORDER BY ''' + string_sort_by +''' ''' + string_sort_order + ''';'''

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



    modified_search = "'%%" + song_search + "%%'"

    query_1 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
      FROM songs, attributes
      WHERE UPPER(name) LIKE UPPER(''' + modified_search + ''') AND song_id = attributes_id;'''

    query_2 = '''SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
      FROM songs, attributes
      WHERE song_id = attributes_id;'''

    song_list = []

    found_song = {'id':0,'name':'none','artist':'none', 'dancaeability':0.0, 'energy':0.0, 'loudness':0.0, 'speechiness':0.0, 'acousticness':0.0, 'liveness':0.0, 'tempo':0.0, 'duration':0.0, 'valence':0.0}

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query_1, (song_search))
        for row in cursor:
            print(row[1])
            found_song = {'id':row[0],'name':row[1],'artist':row[2], 'dancaeability':row[4], 'energy':row[5], 'loudness':row[6], 'speechiness':row[7], 'acousticness':row[8], 'liveness':row[9], 'tempo':row[10], 'duration':row[11], 'valence':row[12]}
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    print(found_song['artist'])

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query_2)
        for row in cursor:
            if row[0] != found_song['id']:
                likeness = (1.0-abs(float(found_song['dancaeability'])-float(row[4])))+(1.0-abs(float(found_song['energy'])-float(row[5])))+(26.8-abs(float(found_song['loudness'])-float(row[6])))/30+(1.0-abs(float(found_song['speechiness'])-float(row[7])))+(1.0-abs(float(found_song['acousticness'])-float(row[8])))/2+(1.0-abs(float(found_song['liveness'])-float(row[9])))/3+(160.0-abs(float(found_song['tempo'])-float(row[10])))/640+(558000.0-abs(float(found_song['duration'])-float(row[11])))/3348000+(1.0-abs(float(found_song['valence'])-float(row[12])))/10
                song = {'id':row[0],'name':row[1],'artist':row[2],'likeness':round(likeness,4)}
                song_list.append(song)

        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    def myFunc(e):
        return e['likeness']

    def second_sort(e):
        # print(string_sort_by)
        return e[string_sort_by]


    song_list.sort(reverse=True, key=myFunc)
    song_list = song_list[0:20]
    song_list.sort(reverse = boolean_sort_order, key=second_sort)

    return json.dumps(song_list)
