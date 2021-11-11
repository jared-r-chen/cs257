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

@api.route('/results<song>')
def get_results():
    ''' Function definition
    '''
    query = '''SELECT * FROM songs,genre, attributes WHERE song = %s'''

    song_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            song_list.append(row)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)
