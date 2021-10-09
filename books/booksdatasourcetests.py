'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
   Author: Jared Chen, Aaron Schondorf
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass
# test one unique author that has an output list of length 1, search by last name
    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))


#test one unique author that has an output list of length 1, search by last name
    def test_unique_author2(self):
        authors = self.data_source.authors('Morrison')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Morrison', 'Toni'))

#test one unique author that has an output list of length 1, search by first name
    def test_author_firstname(self):
        authors = self.data_source.authors('Mary')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Dunnewold', 'Mary'))

#when mutiple authors have the same name, test output count and order
    def test_author_mutiple(self):
        authors = self.data_source.authors('Bront')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))
        self.assertTrue(authors[1] == Author('Brontë', 'Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë', 'Emily'))

#if no input, return a non empty list(that contains all authors)
    def test_author_empty(self):
        authors = self.data_source.authors('')
        self.assertTrue(len(authors) != 0)

#test when there are mutiple authors, and that they are sorted by last name
    def test_author_order(self):
        authors = self.data_source.authors('au')
        self.assertTrue(len(authors) == 2)
        self.assertTrue(authors[0] == Author('Austen', 'Jane'))
        self.assertTrue(authors[1] == Author('Sterne', 'Laurence'))

#test when there are no valid authors
    def test_author_no_result(self):
        authors = self.data_source.authors('auasdfasdfa')
        self.assertTrue(len(authors) == 0)

#test search by book title sorted by title with mutiple results.
    def test_book_bytitle(self):
        books = self.data_source.books('be', 'title')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Beloved'))
        self.assertTrue(books[1] == Book('If Beale Street Could Talk'))

#test search by book title sorted by default with mutiple results.
    def test_book_default(self):
        books = self.data_source.books('be')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Beloved'))
        self.assertTrue(books[1] == Book('If Beale Street Could Talk'))

#test search by book title sorted by default with mutiple results (when no valid sorting method).
    def test_book_default2(self):
        books = self.data_source.books('be', 'adsfagasde')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Beloved'))
        self.assertTrue(books[1] == Book('If Beale Street Could Talk'))

#test search by book title sorted by year with mutiple results.
    def test_book_year(self):
        books = self.data_source.books('be', 'year')
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('If Beale Street Could Talk'))
        self.assertTrue(books[1] == Book('Beloved'))

#test search by book title when no search phrase provided
    def test_book_year(self):
        books = self.data_source.books()
        self.assertTrue(len(books) != 0)

#test search by year with one result
    def test_year(self):
        books_between_years = self.data_source.books_between_years(1919, 1921)
        self.assertTrue(len(books_between_years) == 1)
        self.assertTrue(books_between_years[0] == Book('Main Street'))

#test search by year with one result
    def test_year_inclusive(self):
        books_between_years = self.data_source.books_between_years(1920, 1920)
        self.assertTrue(len(books_between_years) == 1)
        self.assertTrue(books_between_years[0] == Book('Main Street'))

    def test_year_noStart(self):
        books_between_years = self.data_source.books_between_years(None, 1814)
        self.assertTrue(len(books_between_years) == 3)

    def test_year_noStart2(self):
        books_between_years = self.data_source.books_between_years(None, 1814)
        self.assertTrue(len(books_between_years) == 3)
        self.assertTrue(books_between_years[0] == Book('The Life and Opinions of Tristram Shandy, Gentleman'))
        self.assertTrue(books_between_years[1] == Book('Pride and Prejudice'))
        self.assertTrue(books_between_years[2] == Book('Sense and Sensibility'))

    def test_year_noEnd(self):
        books_between_years = self.data_source.books_between_years(2020, None)
        self.assertTrue(len(books_between_years) == 2)

    def test_year_noStart_noEnd(self):
        books_between_years = self.data_source.books_between_years(None, None)
        self.assertTrue(len(books_between_years) != 0)

if __name__ == '__main__':
    unittest.main()
