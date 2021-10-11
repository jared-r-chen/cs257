'''
    books.py
    Aaron Schondorf and Jared Chen, 9 October 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import argparse
from booksdatasource import Author, Book, BooksDataSource

parser = argparse.ArgumentParser()

#mutually exclusive group handles usage of different functions
group = parser.add_mutually_exclusive_group()
group.add_argument('--title', action='store_true', help = 'Search database for books with string in titles. Can be sorted by year or title, determined by the last argument(\'year\' or \'title\'), defaults to title. Example: --title the t year')
group.add_argument('--authors', action='store_true', help = 'Search database for authors with string in author names. Example: --authors bront')
group.add_argument('--years', action='store_true', help = 'Search database for books published between years. Enter years in form startYear-endYear. Example: --years 1990-2001')
#search term that all functions use
parser.add_argument('search', nargs='*')

args = parser.parse_args()
books_data_source = BooksDataSource('books1.csv')
search_list = args.search


if args.title:
    search_term = ''
    num=0
    sort_term = None
    #appends all elements of search_list into search_term
    for num in range(len(search_list)):

        #if final element of search_list is year or title, it will not be added to search_term and be used as sort_term
        if num == len(search_list) - 1:
            if search_list[num] == 'title' or search_list[num] == 'year':
                sort_term = search_list[num]

            else:
                search_term += search_list[num]
        else:
            search_term += search_list[num] + ' '
    if search_term == '':
        search_term = None
    else:
        search_term = search_term.strip()
    books_list = books_data_source.books(search_term, sort_term)
#print results
    for item in books_list:
        print(item.title)


elif args.authors:
    search_term = ''
    #appends all elements of search_list into search_term
    for term in search_list:
        search_term += term +' '
    if search_term == '':
        search_term = None
    else:
        search_term = search_term.strip()
    authors_list = books_data_source.authors(search_term)
# prints out authors results
    for item in authors_list:
        print(item.given_name, end = ' ')
        print(item.surname)

elif args.years:
    #print error message if there are too many arguments
    if len(search_list) > 1:
        print("To many arguments. Type '--help' or '-h' for description of commands supported by this CLI.")
    else:
        start = None
        end = None
        if len(search_list) == 1:
            search_term = search_list[0].strip()
            #uses everything left of - as start year and everything right of - as end year if they exist
            if '-' in search_term:
                if search_term.find('-') != 0:
                    start = int(search_term[0:search_term.find('-')])
                if len(search_term) != search_term.find('-') + 1:
                    end = int(search_term[search_term.find('-') + 1:len(search_term) + 1])
        books_between_years_list = books_data_source.books_between_years(start, end)
#print out books_between_years results
        for item in books_between_years_list:
            print(item.publication_year, end = ' ')
            print(item.title)

else:
    print("Invalid command. Type '--help' or '-h', for description of commands supported by this CLI.")
