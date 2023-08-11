CREATE TABLE IF NOT EXISTS 'verified' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(50) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'rank' varchar (20) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'instructors' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'id' varchar(6) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'volunteers' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'id' varchar(6) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'interns' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'id' varchar(7) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS 'admins' (
  'discord_id' varchar(20) NOT NULL,
  'f_name' varchar(20) NOT NULL,
  'l_name' varchar(50) NOT NULL,
  'id' varchar(6) NOT NULL,
  'key' varchar(64) NOT NULL,
  'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

