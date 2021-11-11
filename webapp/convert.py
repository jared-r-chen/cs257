
'''
    convert.py
    Jared Chen, 11 November 2021

    For use in the "webapp" assignment in CS 257, Software Design class, Fall 2021.

    data for my database is from https://www.kaggle.com/sashankpillai/spotify-top-200-charts-20202021
'''

import csv
# import pandas as pd
#
# df = pd.read_csv (r'/Users/jared.chen/Downloads/olympic_archive/sampleCSV.csv')
# print (df)

def create_songs():
    print('in create_songs')
    filename = "songs.csv"
    song_data = []

    with open('/Users/jared.chen/Downloads/spotify_dataset.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            for row in scanner:
                streams = row[5]
                streams = streams.replace(',', '')

                followers = row[7].strip(' ')
                spotify_id = row[8].strip(' ')
                release_date = row[10].strip(' ')
                popularity = row[12].strip(' ')
                if not followers:
                    # print('index number:', row[0], 'followers:', len(row[7]))

                    #print('error detected')
                    followers = 0
                    spotify_id = 'NA'
                    release_date = 'NA'
                    popularity = 0



                current_row = [row[0], row[1], row[2], row[3], row[4], streams, row[6], followers, spotify_id, release_date, popularity]
                song_data.append(current_row)

    # writing to csv file
    with open(filename, 'w') as csvfile:
        song_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(song_data)

def create_genres():
    print('in create_genres')
    filename = "genres.csv"
    genre_data = []

    with open('/Users/jared.chen/Downloads/spotify_dataset.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            for row in scanner:
                genre_list = []
                current_genre = row[9].strip(' ');
                if not current_genre:
                    current_genre = '[NA]'
                current_genre = current_genre[1:-1]
                genre_list = current_genre.split(',')
                for genre in genre_list:
                    genre = genre.strip(" '")
                    current_row = [row[0], genre]
                    genre_data.append(current_row)

    # writing to csv file
    with open(filename, 'w') as csvfile:
        genre_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(genre_data)

def create_attributes():
    print('in create_attributes')
    filename = "attributes.csv"
    attribute_data = []

    with open('/Users/jared.chen/Downloads/spotify_dataset.csv', newline ='') as csvfile:
            scanner = csv.reader(csvfile, delimiter = ',')
            for row in scanner:
                dancaeability = row[13].strip(' ')
                energy = row[14].strip(' ')
                loudness = row[15].strip(' ')
                speechiness = row[16].strip(' ')
                acousticness = row[17].strip(' ')
                liveness = row[18].strip(' ')
                tempo = row[19].strip(' ')
                duration = row[20].strip(' ')
                valence = row[21].strip(' ')
                chord = row[22].strip(' ')
                if not dancaeability:
                    dancaeability = 0;
                    energy = 0
                    loudness = 0
                    speechiness = 0
                    acousticness = 0
                    liveness = 0
                    tempo = 0
                    duration = 0
                    valence = 0
                    chord = 'NA'

                current_row = [row[0], dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence, chord]
                attribute_data.append(current_row)

    # writing to csv file
    with open(filename, 'w') as csvfile:
        attribute_data.pop(0)
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(attribute_data)

def main():
    create_songs()
    create_genres()
    create_attributes()


if __name__ == "__main__":
    main()
