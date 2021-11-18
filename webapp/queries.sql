--Lists attributes of a given song name. replace Beg with desires search term
SELECT song_id, name, artist, highest_pos, streams
  FROM songs
  WHERE UPPER(name) LIKE UPPER('%beg%')
  ORDER BY name;
--variation on above query
SELECT song_id, name, artist, highest_pos, streams
  FROM songs
  JOIN genres
  ON song_id = genre_id
  WHERE (genre = 'pop') OR (genre = 'alt z')
  ORDER BY name;


  --Gets all genres in the database
  SELECT DISTINCT genre
    FROM genres
    ORDER BY genre;



--the query for songs like function
SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
  FROM songs, attributes
  WHERE UPPER(name) = UPPER(''' + modified_search + ''') AND song_id = attributes_id;

SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
  FROM songs, attributes
  WHERE song_id = attributes_id;
