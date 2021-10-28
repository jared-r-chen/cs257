
CREATE TABLE NOC (
    NOC text,
    country text
);

CREATE TABLE athletes (
    id SERIAL,
    name text,
    NOC text,
    gender text
);

CREATE TABLE events (
    event_id integer,
    id SERIAL,
    year integer,
    sport text,
    event text,
    city text,
    season text,
    medal text
);
