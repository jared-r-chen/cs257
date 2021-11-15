--Lists attributes of a given song name. replace Beg with desires search term
SELECT song_id, name, artist, highest_pos, streams
  FROM songs
  WHERE UPPER(name) LIKE UPPER('%beg%')
  ORDER BY name;

--add a quick comment about what this querie does when you have a minute
SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
  FROM songs, attributes
  WHERE UPPER(name) = UPPER(''' + modified_search + ''') AND song_id = attributes_id;

SELECT song_id, name, artist, attributes_id, dancaeability, energy, loudness, speechiness, acousticness, liveness, tempo, duration, valence
  FROM songs, attributes
  WHERE song_id = attributes_id;
