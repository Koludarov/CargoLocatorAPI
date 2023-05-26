-- migrate:up


CREATE TABLE cargos (
  id SERIAL PRIMARY KEY,
  pickup_location_id INTEGER REFERENCES locations(id),
  delivery_location_id INTEGER REFERENCES locations(id),
  weight INTEGER,
  description TEXT
);




-- migrate:down


DROP TABLE cargos CASCADE;
