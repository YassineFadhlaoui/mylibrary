--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3 (Debian 14.3-1.pgdg110+1)
-- Dumped by pg_dump version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: books; Type: TABLE; Schema: public; Owner: books_manager
--

CREATE TABLE public.books (
    title character varying(1024) NOT NULL,
    author character varying(256),
    cover character varying(2048),
    finished boolean,
    progress integer,
    notes character varying(4096)
);


ALTER TABLE public.books OWNER TO books_manager;

--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: books_manager
--

COPY public.books (title, author, cover, finished, progress, notes) FROM stdin;
the Plague	Albert Camus	static/covers/the_plague.jpeg	t	100
Crime and Punishment	Fyodor Dostoevsky	static/covers/crime_and_punishment.jpg	t	100	Raskolnikov's Crime and Guilt: The story follows Rodion Raskolnikov, a poor ex-student in St. Petersburg who commits a \n        premeditated murder of an unscrupulous pawnbroker. The novel delves into Raskolnikov's internal struggles and the psychological burden of \n        guilt that plagues him.\nThe Dual Nature of Man: Dostoevsky explores the concept of the dual nature of humanity through Raskolnikov's character. Raskolnikov believes in the \nidea of the "extraordinary man" who is exempt from societal and moral laws. However, his crime and subsequent guilt confront him with his own \nvulnerability and his inherent moral compass.
One Hundred Years of Solitude	Gabriel Garcia Marquez	static/covers/one_hundred_years_of_solitude.jpg	t	100	The Buendía Family and Macondo: The story revolves around the Buendía family, tracing their history over several generations. The \n        family is marked by recurring traits, such as solitude, incestuous relationships, and a sense of tragic destiny. Macondo, the town founded \n        by the Buendías, represents a microcosm of the world and undergoes transformation and decay over time.\nTime, Cycles, and Circular History: The narrative is characterized by circular time and repetition, reflecting the idea that history repeats \nitself. Events and patterns reoccur across generations, suggesting a cyclical nature of human existence. The novel explores the concept of eternal \nreturn and the notion that the past continues to shape the present and the future.
The Old Man and the Sea	Ernest Hemingway	static/covers/the_old_man_and_the_sea.jpg	t	100	Santiago's Isolation and Endurance: Santiago is portrayed as a solitary figure, isolated from society and facing physical and \n        emotional hardships. He represents the indomitable human spirit and demonstrates unwavering endurance in his pursuit of the marlin, \n        despite his age and physical limitations. The Battle with the Marlin: The central event of the story is Santiago's battle with the marlin. \n        It becomes a test of his strength, skill, and determination. The struggle is intense and spans several days, showcasing Santiago's \n        resilience and his willingness to confront the challenges of life head-on.
Waiting for Godot	Samuel Beckett	static/covers/waiting_for_godot.jpg	t	100	Existentialism and the Human Condition: The play explores existentialist themes, focusing on the absurdity and meaninglessness of \n        human existence. The characters, Vladimir and Estragon, find themselves trapped in a repetitive and seemingly purposeless cycle of waiting.\nWaiting and Hope: The central theme of the play is waiting for the character Godot, who never arrives. Vladimir and Estragon wait for someone who \nmay provide them with answers or salvation, but their hope is constantly deferred. The waiting becomes a metaphor for the human experience of \nlonging, uncertainty, and the search for meaning.
The Republic	Plato	static/covers/the_republic.jpg	f	76	   The Concept of Justice: Plato explores the nature of justice and argues that it resides in a harmonious balance between different \n        parts of the soul and society. According to him, justice can only be achieved when each individual performs their designated role in society.\nThe Ideal State: Plato proposes the idea of an ideal state, known as the "Kallipolis," ruled by philosopher-kings. He suggests that philosophers, \nwho possess knowledge of the Forms and have the greatest wisdom, should be the rulers and leaders of society. The Allegory of the Cave: Plato uses \nthe allegory of the cave to illustrate his theory of knowledge and the journey of the philosopher. In this allegory, prisoners are confined to a \ndark cave, only seeing shadows on the wall. Plato suggests that true knowledge is attained through philosophical contemplation and the \nunderstanding of the Forms, transcendent and eternal ideals.
don quixote	Miguel de Cervantes	static/covers/don_quixote.jpeg	t	100
anna karenina	Leo Tolstoy	static/covers/anna_karenina.jpeg	t	100
animal farm	George Orwell	static/covers/animal_farm.jpeg	f	99
the trial	franz kafka	static/covers/the_trial.jpeg	t	100
\.


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: books_manager
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (title);


--
-- PostgreSQL database dump complete
--

