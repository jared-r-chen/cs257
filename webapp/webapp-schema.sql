CREATE TABLE songs (
    id integer,
    highest_pos integer,
    times_charted integer,
    top_dates text,
    name text,
    streams integer,
    artist text,
    followers integer,
    spotify_id text,
    release_date text,
    popularity integer
);

CREATE TABLE genres (
    id integer,
    genre text
);

CREATE TABLE attributes (
    id integer,
    dancaeability decimal,
    energy decimal,
    loudness decimal,
    speechiness decimal,
    acousticness decimal,
    liveness decimal,
    tempo decimal,
    duration integer,
    valence decimal,
    chord text
);