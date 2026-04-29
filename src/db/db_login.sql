-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.profile (
  nickname character varying NOT NULL,
  first_name character varying NOT NULL,
  last_name character varying NOT NULL,
  pswd character varying,
  type_id integer,
  CONSTRAINT profile_pkey PRIMARY KEY (nickname),
  CONSTRAINT profile_type_id_fkey FOREIGN KEY (type_id) REFERENCES public.user_type(type_id)
);
CREATE TABLE public.user_type (
  type_id integer NOT NULL DEFAULT nextval('user_type_type_id_seq'::regclass),
  name character varying NOT NULL,
  CONSTRAINT user_type_pkey PRIMARY KEY (type_id)
);

INSERT INTO user_type (type_id, name)
VALUES (
  (1, 'Admin'),
  (2, 'Encargado'),
  (3, 'Gerente'),
);

INSERT INTO profile (nickname, first_name, last_name, pswd, type_id)
VALUES (
  ('DeadTales', 'Carlos', 'Lozano', 'admin1234', 1),
  ('Geno', 'Esau', 'Tapia', 'admin1234', 1),
);