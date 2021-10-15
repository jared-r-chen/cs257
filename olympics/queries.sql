-- List all NOC alphabetically decending
SELECT * FROM NOC
ORDER BY Country ASC;

-- Lists all atheletes from Kenya
SELECT * FROM athletes
WHERE NOC = 'KEN';

-- lists all medals won by Greg Louganis (71665)
SELECT DISTINCT athletes.name, events.event, events.year, events.medal
-- join events and athletes table. distinct removes dups
  FROM events
  JOIN athletes
    ON events.id = athletes.id
-- filter condition is id = 71665 and medals are won
WHERE (medal != 'NA' AND athletes.id = 71665)
ORDER BY year;

-- List all NOC by decending gold medal count
SELECT NOC.country, COUNT(events.medal)
--count gets the number of medals, join three tables together
  FROM NOC
  JOIN athletes
    ON NOC.NOC = athletes.NOC
  JOIN events
    ON athletes.id = events.id
-- filter for gold medals
WHERE (medal = 'Gold')
GROUP BY NOC.country
ORDER BY COUNT(events.medal) DESC;
