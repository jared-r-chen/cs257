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
SELECT DISTINCT unique_events.id, unique_events.year, unique_events.season, unique_events.city
  FROM unique_events
ORDER BY year;

--Lists all NOC with full country name
SELECT DISTINCT * FROM NOC

--Get athletes from an specific olympic game who have won a medal
SELECT DISTINCT athletes.id, athletes.name, athletes.gender, events.sport, events.event, events.medal
  FROM events
  JOIN unique_events
  ON events.year = unique_events.year
  AND events.city = unique_events.city
  AND events.season = unique_events.season
  JOIN athletes
  ON events.id = athletes.id
WHERE (medal != 'NA') AND (unique_events.id = 14)
ORDER BY athletes.name;

--Get athletes from an specific olympic game who have won a medal and are from a specified NOC
SELECT DISTINCT athletes.id, athletes.name, athletes.gender, events.sport, events.event, events.medal
  FROM events
  JOIN unique_events
  ON events.year = unique_events.year
  AND events.city = unique_events.city
  AND events.season = unique_events.season
  JOIN athletes
  ON events.id = athletes.id
WHERE (medal != 'NA') AND (unique_events.id = 14) AND (athletes.NOC = 'CAN')
ORDER BY athletes.name;
