--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2 (Ubuntu 12.2-2.pgdg16.04+1)
-- Dumped by pg_dump version 12.2

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

--
-- Data for Name: antrian_pasien; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.antrian_pasien (id, created_at, durasi_pengobatan, jenis_kelamin, jenis_pengobatan, nama_dokter, nama_pasien, umur, updated_at, waktu_berakhir, waktu_mulai) FROM stdin;
1	2020-04-12 00:52:47.99703+00	14	l	klinik bedah	m lutfi	ada	12	2020-04-12 00:53:01.93696+00	07:53:01	07:52:47
\.


--
-- Name: antrian_antrian_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.antrian_antrian_id_seq', 1, false);


--
-- Name: antrian_antrian_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.antrian_antrian_id_seq1', 1, false);


--
-- PostgreSQL database dump complete
--

