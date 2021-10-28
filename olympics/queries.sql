-- List all NOC alphabetically decending
SELECT * FROM NOC
ORDER BY Country ASC;


-- Lists all atheletes from Kenya
SELECT DISTINCT * FROM athletes
WHERE NOC = 'KEN';


-- lists all medals won by Greg Louganis (71665)
SELECT DISTINCT athletes.name, events.event, events.year, events.medal
  FROM events
  JOIN athletes
    ON events.id = athletes.id
WHERE (medal != 'NA' AND athletes.id = 71665)
ORDER BY year;


-- List all NOC by decending gold medal count
SELECT NOC.country, COUNT(events.medal)
  FROM NOC
  JOIN athletes
    ON NOC.NOC = athletes.NOC
  JOIN events
    ON athletes.id = events.id
WHERE (medal = 'Gold')
GROUP BY NOC.country
ORDER BY COUNT(events.medal) DESC;

--searches athlete names for search string(operation of my choosing)
SELECT DISTINCT * FROM athletes
WHERE LOWER(name) LIKE LOWER('%matt%');

--Lists all games by year decending
SELECT DISTINCT events.event_id, events.year, events.season, events.city
  FROM events
ORDER BY year;
