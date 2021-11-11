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

@api.route('/results<song_search>')
def get_results(song_search):
    ''' Function definition
    '''
    query = '''SELECT * FROM songs,genre,attributes WHERE song = %s'''

    song_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (song_search))
        for row in cursor:
            song = {'id':row[0],'highest_pos':row[1],'times_charted':row[2],'top_dates':row[3],'name':row[4],'streams':row[5],'artist':row[6],'followers':row[7],'spotify_id':row[8],'release_date':row[9],'popularity':row[10]}
            song_list.append(song)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(song_list)
