-- migrate:up


CREATE TABLE trucks (
  id SERIAL PRIMARY KEY,
  uuid VARCHAR(5),
  location_id INTEGER REFERENCES locations(id),
  capacity INTEGER
);


-- migrate:down


DROP TABLE trucks CASCADE;
