-- migrate:up


CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  city VARCHAR,
  state VARCHAR,
  zip_code VARCHAR,
  latitude FLOAT,
  longitude FLOAT
);


CREATE INDEX locations_city_state on locations(city, state);


-- migrate:down


DROP TABLE locations CASCADE;
