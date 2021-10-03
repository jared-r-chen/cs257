import sys
import csv
import argparse
from booksdatasource import Author, Book, BooksDataSource

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('--title', action='store_true', help = "Search database for books with string in titles. Can be sorted by year or title.")
group.add_argument('--authors', action='store_true', help = "Search database for authors with string in author names.")
group.add_argument('--years', action='store_true', help = "Search database for books published between years. Enter years in form startYear-endYear.")
parser.add_argument('search', nargs='+')

args = parser.parse_args()
books_data_source = BooksDataSource('books1.csv')
search_list = args.search
if args.title:
    search_term = ''
    num=0
    sort_term = None
    for num in range(len(search_list)):
        if num == len(search_list):
            if search_list[num] == 'title' or search_list[num] == 'year':
                sort_term = search_list[num]
            else:
                search_term += search_list[num] +' '
    if search_term == '':
        search_term = None
    books_data_source.books(search_term.strip(), sort_term)
elif args.authors:
    search_term = ''
    for term in search_list:
        search_term += term +' '
    if search_term == '':
        search_term = None
    books_data_source.authors(search_term.strip())
elif args.years:
    if len(search_list) > 1:
        print("ERROR! invalid command. type 'help', 'h', or 'usage' for description of commands supported by this CLI.")
    else:
        start = None
        end = None
        if len(search_list) == 1:
            search_term = search_list[0].strip()
            if '-' in search_term:
                if search_term.find('-') != 0:
                    start = int(search_term[0:search_term.find('-')])
                if len(search_term) != search_term.find('-') + 1:
                    end = int(search_term[search_term.find('-') + 1:len(search_term) + 1])
        books_data_source.books_between_years(start, end)
else:
    print("ERROR! invalid command. type 'help', 'h', or 'usage' for description of commands supported by this CLI.")
