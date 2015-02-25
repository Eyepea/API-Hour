CREATE ROLE asterisk LOGIN
ENCRYPTED PASSWORD 'md5120ce93a970c33249f2a1c49cca35557'
NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

CREATE DATABASE benchmarks
WITH OWNER = asterisk
ENCODING = 'UTF8'
TABLESPACE = pg_default
LC_COLLATE = 'en_GB.UTF-8'
LC_CTYPE = 'en_GB.UTF-8'
CONNECTION LIMIT = -1;

CREATE TABLE agent_login_status
(
  agent_id integer NOT NULL,
  agent_number character varying(40) NOT NULL,
  extension character varying(80) NOT NULL,
  context character varying(80) NOT NULL,
  interface character varying(128) NOT NULL,
  state_interface character varying(128) NOT NULL,
  login_at timestamp without time zone NOT NULL DEFAULT now(),
  CONSTRAINT agent_login_status_pkey PRIMARY KEY (agent_id),
  CONSTRAINT agent_login_status_extension_context_key UNIQUE (extension, context),
  CONSTRAINT agent_login_status_interface_key UNIQUE (interface)
)
WITH (
OIDS=FALSE
);
ALTER TABLE agent_login_status
OWNER TO asterisk;

CREATE TABLE agentfeatures
(
  id serial NOT NULL,
  numgroup integer NOT NULL,
  firstname character varying(128) NOT NULL DEFAULT ''::character varying,
  lastname character varying(128) NOT NULL DEFAULT ''::character varying,
  "number" character varying(40) NOT NULL,
  passwd character varying(128) NOT NULL,
  context character varying(39) NOT NULL,
  language character varying(20) NOT NULL,
  autologoff integer,
  "group" character varying(255),
  description text NOT NULL,
  preprocess_subroutine character varying(40),
  CONSTRAINT agentfeatures_pkey PRIMARY KEY (id),
  CONSTRAINT agentfeatures_number_key UNIQUE (number)
)
WITH (
OIDS=FALSE
);
ALTER TABLE agentfeatures
OWNER TO asterisk;

INSERT INTO agentfeatures VALUES (1, 1, 'Stephen', 'Hammen', '300', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (2, 1, 'Lindsay', 'Wheeler', '301', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (3, 1, 'Benjamin', 'French', '302', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (4, 1, 'Ralph', 'Bartko', '303', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (5, 1, 'Jerry', 'Harris', '304', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (6, 1, 'William', 'Anderson', '305', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (7, 1, 'Angela', 'Burrows', '306', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (8, 1, 'John', 'Johnson', '307', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (9, 1, 'Billy', 'Perri', '308', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (10, 1, 'Danny', 'King', '309', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (11, 1, 'Bobby', 'Taylor', '310', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (12, 1, 'Cheryl', 'Brown', '311', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (13, 1, 'Edna', 'Stanley', '312', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (14, 1, 'Roger', 'Morgan', '313', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (15, 1, 'Ray', 'Eoff', '314', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (16, 1, 'Frank', 'Holland', '315', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (17, 1, 'Jolanda', 'Willard', '316', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (18, 1, 'James', 'Williams', '317', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (19, 1, 'Julius', 'Bishop', '318', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (20, 1, 'Tiffany', 'Gillespie', '319', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (21, 1, 'Pamela', 'Ahmed', '320', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (22, 1, 'Bridgett', 'Boyd', '321', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (23, 1, 'Zulema', 'Ruiz', '322', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (24, 1, 'David', 'Fleming', '323', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (25, 1, 'Patricia', 'Miller', '324', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (26, 1, 'Lori', 'Jeffrie', '325', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (27, 1, 'Margaretta', 'Moir', '326', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (28, 1, 'Marie', 'Mix', '327', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (29, 1, 'Francisco', 'Ireland', '328', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (30, 1, 'Colleen', 'Bishop', '329', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (31, 1, 'Mary', 'Cogburn', '330', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (32, 1, 'Richard', 'Rains', '331', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (33, 1, 'Yvonne', 'Williams', '332', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (34, 1, 'Joel', 'Allen', '333', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (35, 1, 'Timothy', 'Merrill', '334', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (36, 1, 'Jimmy', 'Mays', '335', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (37, 1, 'Claire', 'Dean', '336', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (38, 1, 'Sharon', 'Torres', '337', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (39, 1, 'Rhonda', 'Mendez', '338', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (40, 1, 'Jeanne', 'Dilworth', '339', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (41, 1, 'Ruth', 'Jones', '340', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (42, 1, 'Donald', 'Williams', '341', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (43, 1, 'Jason', 'Lux', '342', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (44, 1, 'Jill', 'Barber', '343', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (45, 1, 'Terri', 'Odonnell', '344', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (46, 1, 'Mary', 'Smith', '345', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (47, 1, 'Deborah', 'Landry', '346', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (48, 1, 'Nelson', 'Lesko', '347', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (49, 1, 'Roy', 'Berg', '348', '', 'default', '', 0, '', '', '');
INSERT INTO agentfeatures VALUES (50, 1, 'Elizabeth', 'Ledford', '349', '', 'default', '', 0, '', '', '');

