--
-- PostgreSQL database dump
--

-- Dumped from database version 13.20
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: lucasblack
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist (
    id integer NOT NULL,
    name text NOT NULL,
    realname text,
    profile text,
    data_quality text
);


ALTER TABLE public.artist OWNER TO postgres;

--
-- Name: artist_alias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist_alias (
    artist_id integer NOT NULL,
    alias_name text NOT NULL,
    alias_artist_id integer
);


ALTER TABLE public.artist_alias OWNER TO postgres;

--
-- Name: artist_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist_image (
    artist_id integer NOT NULL,
    type text,
    width integer,
    height integer,
    uri text DEFAULT 'https://i.discogs.com/default-artist.png'::text
);


ALTER TABLE public.artist_image OWNER TO postgres;

--
-- Name: artist_namevariation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist_namevariation (
    id integer NOT NULL,
    artist_id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.artist_namevariation OWNER TO postgres;

--
-- Name: artist_namevariation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_namevariation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.artist_namevariation_id_seq OWNER TO postgres;

--
-- Name: artist_namevariation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_namevariation_id_seq OWNED BY public.artist_namevariation.id;


--
-- Name: artist_url; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artist_url (
    id integer NOT NULL,
    artist_id integer NOT NULL,
    url text NOT NULL
);


ALTER TABLE public.artist_url OWNER TO postgres;

--
-- Name: artist_url_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artist_url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.artist_url_id_seq OWNER TO postgres;

--
-- Name: artist_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artist_url_id_seq OWNED BY public.artist_url.id;


--
-- Name: group_member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_member (
    group_artist_id integer NOT NULL,
    member_artist_id integer NOT NULL,
    member_name text NOT NULL
);


ALTER TABLE public.group_member OWNER TO postgres;

--
-- Name: label; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.label (
    id integer NOT NULL,
    name text NOT NULL,
    contact_info text,
    profile text,
    parent_id integer,
    parent_name text,
    data_quality text
);


ALTER TABLE public.label OWNER TO postgres;

--
-- Name: label_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.label_image (
    label_id integer NOT NULL,
    type text,
    width integer,
    height integer
);


ALTER TABLE public.label_image OWNER TO postgres;

--
-- Name: label_url; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.label_url (
    id integer NOT NULL,
    label_id integer NOT NULL,
    url text NOT NULL
);


ALTER TABLE public.label_url OWNER TO postgres;

--
-- Name: label_url_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.label_url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.label_url_id_seq OWNER TO postgres;

--
-- Name: label_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.label_url_id_seq OWNED BY public.label_url.id;


--
-- Name: master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master (
    id integer NOT NULL,
    title text NOT NULL,
    year integer,
    main_release integer NOT NULL,
    data_quality text
);


ALTER TABLE public.master OWNER TO postgres;

--
-- Name: master_artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master_artist (
    id integer NOT NULL,
    master_id integer NOT NULL,
    artist_id integer NOT NULL,
    artist_name text,
    anv text,
    "position" integer,
    join_string text,
    role text
);


ALTER TABLE public.master_artist OWNER TO postgres;

--
-- Name: master_artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.master_artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.master_artist_id_seq OWNER TO postgres;

--
-- Name: master_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.master_artist_id_seq OWNED BY public.master_artist.id;


--
-- Name: master_genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master_genre (
    id integer NOT NULL,
    master_id integer NOT NULL,
    genre text
);


ALTER TABLE public.master_genre OWNER TO postgres;

--
-- Name: master_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.master_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.master_genre_id_seq OWNER TO postgres;

--
-- Name: master_genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.master_genre_id_seq OWNED BY public.master_genre.id;


--
-- Name: master_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master_image (
    master_id integer NOT NULL,
    type text,
    width integer,
    height integer
);


ALTER TABLE public.master_image OWNER TO postgres;

--
-- Name: master_style; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master_style (
    id integer NOT NULL,
    master_id integer NOT NULL,
    style text
);


ALTER TABLE public.master_style OWNER TO postgres;

--
-- Name: master_style_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.master_style_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.master_style_id_seq OWNER TO postgres;

--
-- Name: master_style_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.master_style_id_seq OWNED BY public.master_style.id;


--
-- Name: master_video; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.master_video (
    id integer NOT NULL,
    master_id integer NOT NULL,
    duration integer,
    title text,
    description text,
    uri text
);


ALTER TABLE public.master_video OWNER TO postgres;

--
-- Name: master_video_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.master_video_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.master_video_id_seq OWNER TO postgres;

--
-- Name: master_video_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.master_video_id_seq OWNED BY public.master_video.id;


--
-- Name: release; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release (
    id integer NOT NULL,
    title text NOT NULL,
    released text,
    country text,
    notes text,
    data_quality text,
    main integer,
    master_id integer,
    status text
);


ALTER TABLE public.release OWNER TO postgres;

--
-- Name: release_artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_artist (
    id integer NOT NULL,
    release_id integer NOT NULL,
    artist_id integer NOT NULL,
    artist_name text,
    extra integer NOT NULL,
    anv text,
    "position" integer,
    join_string text,
    role text,
    tracks text
);


ALTER TABLE public.release_artist OWNER TO postgres;

--
-- Name: release_artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_artist_id_seq OWNER TO postgres;

--
-- Name: release_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_artist_id_seq OWNED BY public.release_artist.id;


--
-- Name: release_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_company (
    id integer NOT NULL,
    release_id integer NOT NULL,
    company_id integer NOT NULL,
    company_name text NOT NULL,
    entity_type text,
    entity_type_name text,
    uri text
);


ALTER TABLE public.release_company OWNER TO postgres;

--
-- Name: release_company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_company_id_seq OWNER TO postgres;

--
-- Name: release_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_company_id_seq OWNED BY public.release_company.id;


--
-- Name: release_format; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_format (
    id integer NOT NULL,
    release_id integer NOT NULL,
    name text,
    qty numeric,
    text_string text,
    descriptions text
);


ALTER TABLE public.release_format OWNER TO postgres;

--
-- Name: release_format_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_format_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_format_id_seq OWNER TO postgres;

--
-- Name: release_format_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_format_id_seq OWNED BY public.release_format.id;


--
-- Name: release_genre; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_genre (
    id integer NOT NULL,
    release_id integer NOT NULL,
    genre text
);


ALTER TABLE public.release_genre OWNER TO postgres;

--
-- Name: release_genre_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_genre_id_seq OWNER TO postgres;

--
-- Name: release_genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_genre_id_seq OWNED BY public.release_genre.id;


--
-- Name: release_identifier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_identifier (
    id integer NOT NULL,
    release_id integer NOT NULL,
    description text,
    type text,
    value text
);


ALTER TABLE public.release_identifier OWNER TO postgres;

--
-- Name: release_identifier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_identifier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_identifier_id_seq OWNER TO postgres;

--
-- Name: release_identifier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_identifier_id_seq OWNED BY public.release_identifier.id;


--
-- Name: release_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_image (
    release_id integer NOT NULL,
    type text,
    width integer,
    height integer
);


ALTER TABLE public.release_image OWNER TO postgres;

--
-- Name: release_label; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_label (
    id integer NOT NULL,
    release_id integer NOT NULL,
    label_id integer,
    label_name text NOT NULL,
    catno text
);


ALTER TABLE public.release_label OWNER TO postgres;

--
-- Name: release_label_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_label_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_label_id_seq OWNER TO postgres;

--
-- Name: release_label_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_label_id_seq OWNED BY public.release_label.id;


--
-- Name: release_style; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_style (
    release_id integer NOT NULL,
    style text
);


ALTER TABLE public.release_style OWNER TO postgres;

--
-- Name: release_track; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_track (
    id integer NOT NULL,
    release_id integer NOT NULL,
    sequence integer NOT NULL,
    "position" text,
    parent integer,
    title text,
    duration text,
    track_id text
);


ALTER TABLE public.release_track OWNER TO postgres;

--
-- Name: release_track_artist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_track_artist (
    id integer NOT NULL,
    track_id text,
    release_id integer NOT NULL,
    track_sequence integer NOT NULL,
    artist_id integer NOT NULL,
    artist_name text,
    extra boolean NOT NULL,
    anv text,
    "position" integer,
    join_string text,
    role text,
    tracks text
);


ALTER TABLE public.release_track_artist OWNER TO postgres;

--
-- Name: release_track_artist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_track_artist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_track_artist_id_seq OWNER TO postgres;

--
-- Name: release_track_artist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_track_artist_id_seq OWNED BY public.release_track_artist.id;


--
-- Name: release_track_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_track_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_track_id_seq OWNER TO postgres;

--
-- Name: release_track_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_track_id_seq OWNED BY public.release_track.id;


--
-- Name: release_video; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.release_video (
    id integer NOT NULL,
    release_id integer NOT NULL,
    duration integer,
    title text,
    description text,
    uri text
);


ALTER TABLE public.release_video OWNER TO postgres;

--
-- Name: release_video_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.release_video_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.release_video_id_seq OWNER TO postgres;

--
-- Name: release_video_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.release_video_id_seq OWNED BY public.release_video.id;


--
-- Name: upcoming_releases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.upcoming_releases (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    artist character varying(255) NOT NULL,
    release_date date NOT NULL,
    additional_info text,
    source_url text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.upcoming_releases OWNER TO postgres;

--
-- Name: upcoming_releases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.upcoming_releases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.upcoming_releases_id_seq OWNER TO postgres;

--
-- Name: upcoming_releases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.upcoming_releases_id_seq OWNED BY public.upcoming_releases.id;


--
-- Name: artist_namevariation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_namevariation ALTER COLUMN id SET DEFAULT nextval('public.artist_namevariation_id_seq'::regclass);


--
-- Name: artist_url id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_url ALTER COLUMN id SET DEFAULT nextval('public.artist_url_id_seq'::regclass);


--
-- Name: label_url id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label_url ALTER COLUMN id SET DEFAULT nextval('public.label_url_id_seq'::regclass);


--
-- Name: master_artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_artist ALTER COLUMN id SET DEFAULT nextval('public.master_artist_id_seq'::regclass);


--
-- Name: master_genre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_genre ALTER COLUMN id SET DEFAULT nextval('public.master_genre_id_seq'::regclass);


--
-- Name: master_style id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_style ALTER COLUMN id SET DEFAULT nextval('public.master_style_id_seq'::regclass);


--
-- Name: master_video id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_video ALTER COLUMN id SET DEFAULT nextval('public.master_video_id_seq'::regclass);


--
-- Name: release_artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_artist ALTER COLUMN id SET DEFAULT nextval('public.release_artist_id_seq'::regclass);


--
-- Name: release_company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_company ALTER COLUMN id SET DEFAULT nextval('public.release_company_id_seq'::regclass);


--
-- Name: release_format id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_format ALTER COLUMN id SET DEFAULT nextval('public.release_format_id_seq'::regclass);


--
-- Name: release_genre id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_genre ALTER COLUMN id SET DEFAULT nextval('public.release_genre_id_seq'::regclass);


--
-- Name: release_identifier id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_identifier ALTER COLUMN id SET DEFAULT nextval('public.release_identifier_id_seq'::regclass);


--
-- Name: release_label id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_label ALTER COLUMN id SET DEFAULT nextval('public.release_label_id_seq'::regclass);


--
-- Name: release_track id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track ALTER COLUMN id SET DEFAULT nextval('public.release_track_id_seq'::regclass);


--
-- Name: release_track_artist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track_artist ALTER COLUMN id SET DEFAULT nextval('public.release_track_artist_id_seq'::regclass);


--
-- Name: release_video id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_video ALTER COLUMN id SET DEFAULT nextval('public.release_video_id_seq'::regclass);


--
-- Name: upcoming_releases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.upcoming_releases ALTER COLUMN id SET DEFAULT nextval('public.upcoming_releases_id_seq'::regclass);


--
-- Name: artist_namevariation artist_namevariation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_namevariation
    ADD CONSTRAINT artist_namevariation_pkey PRIMARY KEY (id);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: artist_url artist_url_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_url
    ADD CONSTRAINT artist_url_pkey PRIMARY KEY (id);


--
-- Name: label label_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label
    ADD CONSTRAINT label_pkey PRIMARY KEY (id);


--
-- Name: label_url label_url_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label_url
    ADD CONSTRAINT label_url_pkey PRIMARY KEY (id);


--
-- Name: master_artist master_artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_artist
    ADD CONSTRAINT master_artist_pkey PRIMARY KEY (id);


--
-- Name: master_genre master_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_genre
    ADD CONSTRAINT master_genre_pkey PRIMARY KEY (id);


--
-- Name: master master_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master
    ADD CONSTRAINT master_pkey PRIMARY KEY (id);


--
-- Name: master_style master_style_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_style
    ADD CONSTRAINT master_style_pkey PRIMARY KEY (id);


--
-- Name: master_video master_video_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_video
    ADD CONSTRAINT master_video_pkey PRIMARY KEY (id);


--
-- Name: release_artist release_artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_artist
    ADD CONSTRAINT release_artist_pkey PRIMARY KEY (id);


--
-- Name: release_company release_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_company
    ADD CONSTRAINT release_company_pkey PRIMARY KEY (id);


--
-- Name: release_format release_format_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_format
    ADD CONSTRAINT release_format_pkey PRIMARY KEY (id);


--
-- Name: release_genre release_genre_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_genre
    ADD CONSTRAINT release_genre_pkey PRIMARY KEY (id);


--
-- Name: release_identifier release_identifier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_identifier
    ADD CONSTRAINT release_identifier_pkey PRIMARY KEY (id);


--
-- Name: release_label release_label_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_label
    ADD CONSTRAINT release_label_pkey PRIMARY KEY (id);


--
-- Name: release release_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release
    ADD CONSTRAINT release_pkey PRIMARY KEY (id);


--
-- Name: release_track_artist release_track_artist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track_artist
    ADD CONSTRAINT release_track_artist_pkey PRIMARY KEY (id);


--
-- Name: release_track release_track_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track
    ADD CONSTRAINT release_track_pkey PRIMARY KEY (id);


--
-- Name: release_video release_video_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_video
    ADD CONSTRAINT release_video_pkey PRIMARY KEY (id);


--
-- Name: upcoming_releases unique_title_artist; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.upcoming_releases
    ADD CONSTRAINT unique_title_artist UNIQUE (title, artist);


--
-- Name: upcoming_releases upcoming_releases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.upcoming_releases
    ADD CONSTRAINT upcoming_releases_pkey PRIMARY KEY (id);


--
-- Name: artist_alias_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX artist_alias_idx_artist ON public.artist_alias USING btree (artist_id);


--
-- Name: artist_namevariation_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX artist_namevariation_idx_artist ON public.artist_namevariation USING btree (artist_id);


--
-- Name: artist_url_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX artist_url_idx_artist ON public.artist_url USING btree (artist_id);


--
-- Name: group_member_idx_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX group_member_idx_group ON public.group_member USING btree (group_artist_id);


--
-- Name: group_member_idx_member; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX group_member_idx_member ON public.group_member USING btree (member_artist_id);


--
-- Name: label_idx_parent_label; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX label_idx_parent_label ON public.label USING btree (parent_id);


--
-- Name: label_url_idx_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX label_url_idx_url ON public.label_url USING btree (label_id);


--
-- Name: master_artist_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX master_artist_idx_artist ON public.master_artist USING btree (artist_id);


--
-- Name: master_artist_idx_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX master_artist_idx_master ON public.master_artist USING btree (master_id);


--
-- Name: master_genre_idx_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX master_genre_idx_master ON public.master_genre USING btree (master_id);


--
-- Name: master_style_idx_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX master_style_idx_master ON public.master_style USING btree (master_id);


--
-- Name: master_video_idx_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX master_video_idx_master ON public.master_video USING btree (master_id);


--
-- Name: release_artist_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_artist_idx_artist ON public.release_artist USING btree (artist_id);


--
-- Name: release_artist_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_artist_idx_release ON public.release_artist USING btree (release_id);


--
-- Name: release_company_idx_company; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_company_idx_company ON public.release_company USING btree (company_id);


--
-- Name: release_company_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_company_idx_release ON public.release_company USING btree (release_id);


--
-- Name: release_format_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_format_idx_release ON public.release_format USING btree (release_id);


--
-- Name: release_genre_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_genre_idx_release ON public.release_genre USING btree (release_id);


--
-- Name: release_identifier_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_identifier_idx_release ON public.release_identifier USING btree (release_id);


--
-- Name: release_idx_master; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_idx_master ON public.release USING btree (master_id);


--
-- Name: release_label_idx_label; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_label_idx_label ON public.release_label USING btree (label_id);


--
-- Name: release_label_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_label_idx_release ON public.release_label USING btree (release_id);


--
-- Name: release_style_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_style_idx_release ON public.release_style USING btree (release_id);


--
-- Name: release_track_artist_idx_artist; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_artist_idx_artist ON public.release_track_artist USING btree (artist_id);


--
-- Name: release_track_artist_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_artist_idx_release ON public.release_track_artist USING btree (release_id);


--
-- Name: release_track_artist_idx_track_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_artist_idx_track_id ON public.release_track_artist USING btree (track_id);


--
-- Name: release_track_artist_idx_track_sequence; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_artist_idx_track_sequence ON public.release_track_artist USING btree (track_sequence);


--
-- Name: release_track_idx_parent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_idx_parent ON public.release_track USING btree (parent);


--
-- Name: release_track_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_idx_release ON public.release_track USING btree (release_id);


--
-- Name: release_track_idx_sequence; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_track_idx_sequence ON public.release_track USING btree (sequence);


--
-- Name: release_video_idx_release; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX release_video_idx_release ON public.release_video USING btree (release_id);


--
-- Name: artist_alias artist_alias_fk_alias_artist; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_alias
    ADD CONSTRAINT artist_alias_fk_alias_artist FOREIGN KEY (alias_artist_id) REFERENCES public.artist(id);


--
-- Name: artist_alias artist_alias_fk_artist; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_alias
    ADD CONSTRAINT artist_alias_fk_artist FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: artist_namevariation artist_namevariation_fk_artist; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_namevariation
    ADD CONSTRAINT artist_namevariation_fk_artist FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: artist_url artist_url_fk_artist; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artist_url
    ADD CONSTRAINT artist_url_fk_artist FOREIGN KEY (artist_id) REFERENCES public.artist(id);


--
-- Name: group_member group_member_fk_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_member
    ADD CONSTRAINT group_member_fk_group FOREIGN KEY (group_artist_id) REFERENCES public.artist(id);


--
-- Name: label label_fk_parent_label; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label
    ADD CONSTRAINT label_fk_parent_label FOREIGN KEY (parent_id) REFERENCES public.label(id);


--
-- Name: label_url label_url_fk_label; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label_url
    ADD CONSTRAINT label_url_fk_label FOREIGN KEY (label_id) REFERENCES public.label(id);


--
-- Name: master_artist master_artist_fk_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_artist
    ADD CONSTRAINT master_artist_fk_master FOREIGN KEY (master_id) REFERENCES public.master(id);


--
-- Name: master_genre master_genre_fk_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_genre
    ADD CONSTRAINT master_genre_fk_master FOREIGN KEY (master_id) REFERENCES public.master(id);


--
-- Name: master_style master_style_fk_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_style
    ADD CONSTRAINT master_style_fk_master FOREIGN KEY (master_id) REFERENCES public.master(id);


--
-- Name: master_video master_video_fk_master; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.master_video
    ADD CONSTRAINT master_video_fk_master FOREIGN KEY (master_id) REFERENCES public.master(id);


--
-- Name: release_artist release_artist_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_artist
    ADD CONSTRAINT release_artist_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_company release_company_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_company
    ADD CONSTRAINT release_company_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_format release_format_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_format
    ADD CONSTRAINT release_format_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_genre release_genre_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_genre
    ADD CONSTRAINT release_genre_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_identifier release_identifier_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_identifier
    ADD CONSTRAINT release_identifier_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_label release_label_fk_label; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_label
    ADD CONSTRAINT release_label_fk_label FOREIGN KEY (label_id) REFERENCES public.label(id);


--
-- Name: release_label release_label_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_label
    ADD CONSTRAINT release_label_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_style release_style_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_style
    ADD CONSTRAINT release_style_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_track_artist release_track_artist_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track_artist
    ADD CONSTRAINT release_track_artist_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_track release_track_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_track
    ADD CONSTRAINT release_track_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: release_video release_video_fk_release; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.release_video
    ADD CONSTRAINT release_video_fk_release FOREIGN KEY (release_id) REFERENCES public.release(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: lucasblack
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

INSERT INTO public.artist (id, name, realname, profile, data_quality) VALUES 
(12345, 'Test Artist', 'Real Test Artist', 'Test artist profile', 'Correct'),
(23456, 'Test Artist 2', 'Real Test Artist 2', 'Another test artist profile', 'Correct'),
(34567, 'The Beatles', 'John, Paul, George, Ringo', 'Famous British rock band', 'Correct'),
(45678, 'David Bowie', 'David Robert Jones', 'British musician and actor', 'Correct'),
(56789, 'Miles Davis', 'Miles Dewey Davis III', 'American jazz trumpeter', 'Correct');

-- Insert test data for masters
INSERT INTO public.master (id, title, year, main_release, data_quality) VALUES
(12345, 'Test Master', 2020, 12345, 'Correct'),
(23456, 'Abbey Road', 1969, 23456, 'Correct'),
(34567, 'Test Album 1', 2020, 34567, 'Correct'),
(45678, 'Test Album 2', 2021, 45678, 'Correct'),
(56789, 'Kind of Blue', 1959, 56789, 'Correct');

INSERT INTO public.master_artist (id, master_id, artist_id, artist_name) VALUES
(1, 12345, 12345, 'Test Artist');

INSERT INTO public.master_style (id, master_id, style) VALUES
(1, 12345, 'Thrash');

INSERT INTO public.master_genre (id, master_id, genre) VALUES
(1, 12345, 'Rock');

-- Insert test data for releases
INSERT INTO public.release (id, title, released, country, notes, data_quality, master_id, status) VALUES
(12345, 'Test Release', '2020', 'US', 'Test release notes', 'Correct', 12345, 'Official'),
(23456, 'Abbey Road', '1969-09-26', 'UK', 'The Beatles album', 'Correct', 23456, 'Official'),
(34567, 'Test Album 1', '2020-01-01', 'US', 'Test album notes', 'Correct', 34567, 'Official'),
(45678, 'Test Album 2', '2021-06-15', 'UK', 'Another test album', 'Correct', 45678, 'Official'),
(56789, 'Kind of Blue', '1959-08-17', 'US', 'Classic jazz album', 'Correct', 56789, 'Official');

-- Insert test data for release_track
INSERT INTO public.release_track (id, release_id, sequence, title, duration) VALUES
(1, 12345, 1, 'Test Track', '3:45'),
(2, 23456, 1, 'Come Together', '4:20'),
(3, 23456, 2, 'Something', '3:03'),
(4, 34567, 1, 'Test Track 1', '4:30'),
(5, 45678, 1, 'Test Track 2', '3:22'),
(6, 56789, 1, 'So What', '9:22');
