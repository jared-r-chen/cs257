import argparse
import psycopg2

from config import password
from config import database
from config import user

try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()

try:
    cursor = connection.cursor()
except Exception as e:
    print(e)
    exit()

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('--golds', action='store_true', help = 'List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.')
group.add_argument('--athletes', action='store_true', help = 'List the names of all the athletes from a specifc NOC (NOC abreviation should be listed after --athletes command)')
group.add_argument('--name', action='store_true', help = 'List the names of all the athletes with the search term in their name (search term should be listed after --name command)')
#search term
parser.add_argument('search', nargs= '*' )

args = parser.parse_args()

if args.golds:
    query = '''SELECT NOC.country, COUNT(events.medal)
            FROM NOC
            JOIN athletes
            ON NOC.NOC = athletes.NOC
            JOIN events
            ON athletes.id = events.id
            WHERE (medal = 'Gold')
            GROUP BY NOC.country
            ORDER BY COUNT(events.medal) DESC'''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    print('============ Countries and Gold Medal Counts ============')
    print('Country, Gold Medals')
    for row in cursor:
        print(row[0], row[1])
    print()

elif args.athletes:
    search_string = args.search[0]
    print(search_string)
    search_string = search_string.upper()

    query = '''SELECT DISTINCT * FROM athletes
            WHERE NOC = %s'''
    try:
        cursor.execute(query, (search_string,))
    except Exception as e:
        print(e)
        exit()

    print('============ Athletes From {0} ============'.format(search_string))
    print('ID number, Name, NOC')
    for row in cursor:
        print(row[0], row[1], row[2])
    print()

elif args.name:
    search_string = args.search[0]

#this line underneath is needed so sql knows the searchstring should be a substring
    modded_search_string = '%' + search_string + '%'

    query = '''SELECT DISTINCT * FROM athletes
    WHERE LOWER(name) LIKE LOWER(%s)'''
    try:
        cursor.execute(query, (modded_search_string,))
    except Exception as e:
        print(e)
        exit()

    print('============ Names Containing {0} ============'.format(search_string))
    print('ID number, Name, NOC')
    for row in cursor:
        print(row[0], row[1], row[2])
    print()

else:
    print("Invalid command. Type '--help' or '-h', for description of commands supported by this CLI.")
