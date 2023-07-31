CREATE TABLE IF NOT EXISTS 'verified' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(50) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'jei_id' varchar(6) NOT NULL,
  'age' varchar(3) NOT NULL,
  'rank' varchar (20) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

r
