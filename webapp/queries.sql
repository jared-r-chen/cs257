--Lists attributes of a given song name. replace Beg with desires search term
SELECT id, name, artist, highest_pos, streams
  FROM songs
  WHERE UPPER(name) LIKE UPPER('%beg%')
  ORDER BY name;
