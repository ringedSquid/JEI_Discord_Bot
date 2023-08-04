CREATE TABLE IF NOT EXISTS 'verified' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(50) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'age' varchar(3) NOT NULL,
  'rank' varchar (20) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'instructors' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'jei_id' varchar(6) NOT NULL,
  'age' varchar(3) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS 'interns' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'syep_id' varchar(12) NOT NULL,
  'age' varchar(3) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)

