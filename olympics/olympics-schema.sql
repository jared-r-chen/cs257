
CREATE TABLE NOC (
    NOC text,
    country text
);

CREATE TABLE athletes (
    id SERIAL,
    name text,
    NOC text
);

CREATE TABLE events (
    id integer,
    year integer,
    sport text,
    event text,
    medal text
);
