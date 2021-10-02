import sys
import csv
import argparse
import booksdatasource

def parse_command_line(self):

    parser = argparse.ArgumentParser()

    parser.addArguement("input", help = "phrase to determine what happens next")
    parser.addArguement("arg1", help = "first potential user input")
    parser.addArguement("arg2", help = "second potential user input")

    args = parser.parse_args()

    if args.input == 'h' or args.input == 'help' or args.input == 'usage':
        for line in open('usage.txt').readlines():
			print(line, end='')

    elif args.input == 'title':
        self.books(args.arg1)
    elif args.input == 'authors':
        self.authors(args.arg1)
    elif args.input == 'years':
        self.books_between_years(args.arg1, args.arg2)
    else:
        print("ERROR! invalid command. type 'help', 'h', or 'usage' for description of commands supported by this CLI.")
