#!/usr/bin/env python3
'''
    olympics-api.py
    Jared Chen, 27 October 2021

     implement an API based on the Olympics database.
'''
import sys
import argparse
import flask
import json
import psycopg2

from config import password
from config import database
from config import user

app = flask.Flask(__name__)

def connect_to_database():
    '''connects to database specified in config file'''
    from config import password
    from config import database
    from config import user

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()

def execute_query(query, connection):
    '''executes a query where ther query and database connection are parameters'''
    try:
        cursor = connection.cursor()
        this_query = query
        cursor.execute(this_query)
        return cursor
    except Exception as e:
        print(e)
        exit()

def create_games_dict(connection):
    query = '''SELECT DISTINCT unique_events.id, unique_events.year, unique_events.season, unique_events.city
            FROM unique_events
            ORDER BY year;'''
    games_list = []
    cursor = execute_query(query, connection)
    for row in cursor:
        games_list.append({'id': row[0], 'year': row[1], 'season': row[3], 'city': row[2]})
    return games_list

def create_noc_dict(connection):
    query = '''SELECT DISTINCT * FROM NOC;'''
    noc_list = []
    cursor = execute_query(query, connection)
    for row in cursor:
        noc_list.append({'NOC': row[0], 'name': row[1]})
    return noc_list

def create_medalist_query(connection, games_id):
    query = '''SELECT DISTINCT athletes.id, athletes.name, athletes.gender, events.sport, events.event, events.medal
      FROM events
      JOIN unique_events
      ON events.year = unique_events.year
      AND events.city = unique_events.city
      AND events.season = unique_events.season
      JOIN athletes
      ON events.id = athletes.id
    WHERE (medal != 'NA') AND (unique_events.id = ''' + games_id + ''')
    ORDER BY athletes.name;'''
    medalist_list = []
    cursor = execute_query(query, connection)
    for row in cursor:
        medalist_list.append({'athlete_id': row[0], 'name': row[1], 'sex': row[2], 'sport': row[3], 'event': row[4], 'medal': row[5]})
    return medalist_list

def create_medalist_noc_query(connection, games_id, noc):
    modded_noc = '\'' + noc + '\''
    query = '''SELECT DISTINCT athletes.id, athletes.name, athletes.gender, events.sport, events.event, events.medal
      FROM events
      JOIN unique_events
      ON events.year = unique_events.year
      AND events.city = unique_events.city
      AND events.season = unique_events.season
      JOIN athletes
      ON events.id = athletes.id
    WHERE (medal != 'NA') AND (unique_events.id = ''' + games_id + ''') AND (athletes.NOC = ''' + modded_noc + ''')
    ORDER BY athletes.name;'''
    medalist_list = []
    cursor = execute_query(query, connection)
    for row in cursor:
        medalist_list.append({'athlete_id': row[0], 'name': row[1], 'sex': row[2], 'sport': row[3], 'event': row[4], 'medal': row[5]})
    return medalist_list


@app.route('/')
def hello():
    return 'Welcome to my olympics API'

@app.route('/games')
def get_games():
    games_list = []
    connection = connect_to_database()
    for game in create_games_dict(connection):
        games_list.append(game)
    return json.dumps(games_list)

@app.route('/nocs')
def get_noc():
    noc_list = []
    connection = connect_to_database()
    for noc in create_noc_dict(connection):
        noc_list.append(noc)
    return json.dumps(noc_list)

@app.route('/medalists/games/<games_id>')
def get_medalist_noc(games_id):
    medalist_list = []
    connection = connect_to_database()
    noc = flask.request.args.get('noc')
    string_noc = str(noc)
    if noc:
        for medalist in create_medalist_noc_query(connection, games_id, string_noc):
            medalist_list.append(medalist)
    else:
        for medalist in create_medalist_query(connection, games_id):
            medalist_list.append(medalist)
    return json.dumps(medalist_list)




if __name__ == '__main__':
    parser = argparse.ArgumentParser('olympics flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
