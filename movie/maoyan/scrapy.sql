DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS movie_type;
DROP TABLE IF EXISTS movie_actor;

CREATE TABLE movies(
  'id' INTEGER PRIMARY KEY NOT NULL,
  'name' TEXT,
  'director' TEXT,
  'box_office' INTEGER,
  'date' TEXT,
  'score' REAL
);

CREATE TABLE types(
  'id' INTEGER PRIMARY KEY NOT NULL,
  'name' TEXT UNIQUE NOT NULL
);

CREATE TABLE actors(
  'id' INTEGER PRIMARY KEY NOT NULL,
  'name' TEXT UNIQUE NOT NULL
);

CREATE TABLE movie_type(
  'movie_id' INTEGER,
  'type_id' INTEGER,
  FOREIGN KEY(movie_id) REFERENCES movies(id) ON DELETE CASCADE,
  FOREIGN KEY(type_id) REFERENCES types(id) ON DELETE CASCADE
);

CREATE TABLE movie_actor(
  'movie_id' INTEGER,
  'actor_id' INTEGER,
  FOREIGN KEY(movie_id) REFERENCES movies(id) ON DELETE CASCADE,
  FOREIGN KEY(actor_id) REFERENCES actors(id) ON DELETE CASCADE
);
