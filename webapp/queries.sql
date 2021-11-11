--Lists attributes of a given song name. replace Beg with desires search term
SELECT name, artist, highest_pos, streams
  FROM songs
  WHERE name LIKE '%Beg%'
  ORDER BY name;
