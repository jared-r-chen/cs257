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

    query = '''SELECT id, name, artist, highest_pos, streams
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
            song = {'id':row[0],'name':row[1],'artist':row[2],'highest position':row[3],'streams':row[4]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)
