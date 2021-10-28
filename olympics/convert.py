
'''
    convert.py
    Jared Chen, 14 October 2021

    For use in the "olympics" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.

    data for my database is from https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv
# import pandas as pd
#
# df = pd.read_csv (r'/Users/jared.chen/Downloads/olympic_archive/sampleCSV.csv')
# print (df)

def create_NOC():
    print('in create_NOC')
    filename = "NOC.csv"
    NOC_data = []

    with open('/Users/jared.chen/Downloads/olympic_archive/noc_regions.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            for row in scanner:
                current_row = [row[0], row[1]]
                NOC_data.append(current_row)

    # writing to csv file
    with open(filename, 'w') as csvfile:
        NOC_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(NOC_data)


def create_athletes():
    print('in create create_athletes')
    filename = "athletes.csv"
    athlete_data = []

    with open('/Users/jared.chen/Downloads/olympic_archive/athlete_events.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            for row in scanner:
                current_row = [row[0], row[1], row[7], row[2]]
                athlete_data.append(current_row)

    # writing to csv file
    with open(filename, 'w') as csvfile:
        athlete_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(athlete_data)


def create_events():
    print('in create_events')
    filename = "events.csv"
    event_data = []

    with open('/Users/jared.chen/Downloads/olympic_archive/athlete_events.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            curr_id = 0
            for row in scanner:
                current_row = [curr_id, row[0], row[9], row[12], row[13], row[11], row[14]]
                event_data.append(current_row)
                curr_id = curr_id + 1;

    # writing to csv file
    with open(filename, 'w') as csvfile:
        event_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(event_data)

def main():
    create_NOC()
    create_athletes()
    create_events()

if __name__ == "__main__":
    main()
