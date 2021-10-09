#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''

        self.init_book_list = []
        with open(books_csv_file_name, newline ='') as csvfile:
            book_reader = csv.reader(csvfile, delimiter = ',')
            for row in book_reader:
                set_author_list = []
                counter = 0;
                for i in row[2]:
                    if i == '(':
                        counter = counter + 1
                    tempString = row[2]
                for x in range(counter):
                    curAuthor = tempString[0: tempString.find(')') + 1]
                    fullName = curAuthor[0:curAuthor.find('(')]
                    wordList = fullName.split()
                    lastName = wordList[-1]
                    firstName = fullName[:fullName.find(lastName)]
                    birthDate = int(curAuthor[curAuthor.find('(') + 1:curAuthor.find('-')])
                    deathDate = None
                    if curAuthor.find('-') + 1 != curAuthor.find(')'):
                        deathDate = int(curAuthor[curAuthor.find('-') + 1:curAuthor.find(')')])
                    author = Author(lastName.strip(), firstName.strip(), birthDate, deathDate)
                    set_author_list.append(author)
                book = Book(row[0], int(row[1]), set_author_list)
                self.init_book_list.append(book)

                if tempString:
                    tempString = tempString[tempString.find(')') + 6:]

        pass

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authors_list = []

        if search_text == None:
            for book in self.init_book_list:
                for current_author in book.authors:
                    if authors_list.count(current_author) == 0:
                        authors_list.append(current_author)
        else:
            for book in self.init_book_list:
                for current_author in book.authors:
                    if search_text.lower() in current_author.surname.lower() + ' ' + current_author.given_name.lower():
                        if authors_list.count(current_author) == 0:
                            authors_list.append(current_author)

        def authors_sort_func(e):
            return e.surname + ' ' + e.given_name

        authors_list.sort(key = authors_sort_func)

        for item in authors_list:
            print(item.given_name, end = ' ')
            print(item.surname)

        return authors_list

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        books_list = []

        if search_text == None:
            for book in self.init_book_list:
                books_list.append(book)
        else:
            for book in self.init_book_list:
                if search_text.lower() in book.title.lower():
                    books_list.append(book)

        def books_sort_func(e):
            if sort_by == 'year':
                my_key = e.publication_year
            else:
                my_key = e.title
            return my_key

        books_list.sort(key = books_sort_func)

        for item in books_list:
            print(item.title)

        return books_list

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''

        books_between_years_list = []

        if start_year == None:
            start_year = 1500
        if end_year == None:
            end_year = 2050

        def year_sort_func(e):
            return e.title

        for year in range(start_year, end_year+1):
            year_list = []
            for book in self.init_book_list:
                if book.publication_year == year:
                    year_list.append(book)
            year_list.sort(key = year_sort_func)
            books_between_years_list += year_list

        for item in books_between_years_list:
            print(item.publication_year, end = ' ')
            print(item.title)

        return books_between_years_list
