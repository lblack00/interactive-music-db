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
-- Name: email_verification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email_verification (
    user_id integer NOT NULL,
    verification_token character varying(100) NOT NULL,
    token_expiry timestamp with time zone NOT NULL,
    is_verified boolean DEFAULT false
);


ALTER TABLE public.email_verification OWNER TO postgres;

--
-- Name: forum_references; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forum_references (
    id integer NOT NULL,
    item_type character varying(50) NOT NULL,
    item_id integer NOT NULL,
    reference_type character varying(50) NOT NULL,
    reference_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    name character varying(255)
);


ALTER TABLE public.forum_references OWNER TO postgres;

--
-- Name: forum_references_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forum_references_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forum_references_id_seq OWNER TO postgres;

--
-- Name: forum_references_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forum_references_id_seq OWNED BY public.forum_references.id;


--
-- Name: forum_replies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forum_replies (
    id integer NOT NULL,
    thread_id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL,
    parent_id integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    is_edited boolean DEFAULT false,
    is_deleted boolean DEFAULT false
);


ALTER TABLE public.forum_replies OWNER TO postgres;

--
-- Name: forum_replies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forum_replies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forum_replies_id_seq OWNER TO postgres;

--
-- Name: forum_replies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forum_replies_id_seq OWNED BY public.forum_replies.id;


--
-- Name: forum_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forum_reports (
    id integer NOT NULL,
    user_id integer NOT NULL,
    item_type character varying(50) NOT NULL,
    item_id integer NOT NULL,
    reason text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    resolved boolean DEFAULT false,
    resolved_by integer,
    resolved_at timestamp with time zone
);


ALTER TABLE public.forum_reports OWNER TO postgres;

--
-- Name: forum_reports_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forum_reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forum_reports_id_seq OWNER TO postgres;

--
-- Name: forum_reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forum_reports_id_seq OWNED BY public.forum_reports.id;


--
-- Name: forum_threads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forum_threads (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    is_edited boolean DEFAULT false,
    is_deleted boolean DEFAULT false,
    category character varying(127)
);


ALTER TABLE public.forum_threads OWNER TO postgres;

--
-- Name: forum_threads_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.forum_threads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.forum_threads_id_seq OWNER TO postgres;

--
-- Name: forum_threads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.forum_threads_id_seq OWNED BY public.forum_threads.id;


--
-- Name: listening_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.listening_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    master_id integer NOT NULL,
    duration_hours numeric(10,2) NOT NULL,
    listened_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.listening_history OWNER TO postgres;

--
-- Name: listening_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.listening_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.listening_history_id_seq OWNER TO postgres;

--
-- Name: listening_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.listening_history_id_seq OWNED BY public.listening_history.id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_tokens (
    user_id integer NOT NULL,
    token character varying(100) NOT NULL,
    expiry timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.password_reset_tokens OWNER TO postgres;

--
-- Name: ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ratings (
    id integer NOT NULL,
    user_id integer NOT NULL,
    item_type character varying(10) NOT NULL,
    item_id character varying(50) NOT NULL,
    rating numeric(3,1) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_item_type CHECK (((item_type)::text = ANY ((ARRAY['artist'::character varying, 'master'::character varying, 'release'::character varying])::text[]))),
    CONSTRAINT valid_rating CHECK (((rating >= (1)::numeric) AND (rating <= (10)::numeric)))
);


ALTER TABLE public.ratings OWNER TO postgres;

--
-- Name: ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ratings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ratings_id_seq OWNER TO postgres;

--
-- Name: ratings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ratings_id_seq OWNED BY public.ratings.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    is_admin boolean DEFAULT false,
    bio character varying(500)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: forum_references id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_references ALTER COLUMN id SET DEFAULT nextval('public.forum_references_id_seq'::regclass);


--
-- Name: forum_replies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_replies ALTER COLUMN id SET DEFAULT nextval('public.forum_replies_id_seq'::regclass);


--
-- Name: forum_reports id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_reports ALTER COLUMN id SET DEFAULT nextval('public.forum_reports_id_seq'::regclass);


--
-- Name: forum_threads id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_threads ALTER COLUMN id SET DEFAULT nextval('public.forum_threads_id_seq'::regclass);


--
-- Name: listening_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listening_history ALTER COLUMN id SET DEFAULT nextval('public.listening_history_id_seq'::regclass);


--
-- Name: ratings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings ALTER COLUMN id SET DEFAULT nextval('public.ratings_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: email_verification email_verification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_verification
    ADD CONSTRAINT email_verification_pkey PRIMARY KEY (user_id);


--
-- Name: forum_references forum_references_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_references
    ADD CONSTRAINT forum_references_pkey PRIMARY KEY (id);


--
-- Name: forum_replies forum_replies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_replies
    ADD CONSTRAINT forum_replies_pkey PRIMARY KEY (id);


--
-- Name: forum_reports forum_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_reports
    ADD CONSTRAINT forum_reports_pkey PRIMARY KEY (id);


--
-- Name: forum_threads forum_threads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_threads
    ADD CONSTRAINT forum_threads_pkey PRIMARY KEY (id);


--
-- Name: listening_history listening_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listening_history
    ADD CONSTRAINT listening_history_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (user_id);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (id);


--
-- Name: ratings ratings_user_id_item_type_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_user_id_item_type_item_id_key UNIQUE (user_id, item_type, item_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_forum_references_item; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_forum_references_item ON public.forum_references USING btree (item_type, item_id);


--
-- Name: idx_forum_references_ref; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_forum_references_ref ON public.forum_references USING btree (reference_type, reference_id);


--
-- Name: idx_forum_replies_parent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_forum_replies_parent_id ON public.forum_replies USING btree (parent_id);


--
-- Name: idx_forum_replies_thread_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_forum_replies_thread_id ON public.forum_replies USING btree (thread_id);


--
-- Name: idx_forum_reports_item; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_forum_reports_item ON public.forum_reports USING btree (item_type, item_id);


--
-- Name: idx_listening_history_master_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_listening_history_master_id ON public.listening_history USING btree (master_id);


--
-- Name: idx_listening_history_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_listening_history_user_id ON public.listening_history USING btree (user_id);


--
-- Name: email_verification email_verification_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_verification
    ADD CONSTRAINT email_verification_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: forum_replies forum_replies_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_replies
    ADD CONSTRAINT forum_replies_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.forum_replies(id);


--
-- Name: forum_replies forum_replies_thread_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_replies
    ADD CONSTRAINT forum_replies_thread_id_fkey FOREIGN KEY (thread_id) REFERENCES public.forum_threads(id);


--
-- Name: forum_replies forum_replies_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_replies
    ADD CONSTRAINT forum_replies_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: forum_reports forum_reports_resolved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_reports
    ADD CONSTRAINT forum_reports_resolved_by_fkey FOREIGN KEY (resolved_by) REFERENCES public.users(id);


--
-- Name: forum_reports forum_reports_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_reports
    ADD CONSTRAINT forum_reports_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: forum_threads forum_threads_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forum_threads
    ADD CONSTRAINT forum_threads_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: listening_history listening_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listening_history
    ADD CONSTRAINT listening_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: lucasblack
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

INSERT INTO public.users (id, username, email, password, is_admin, bio) VALUES
(1, 'Test User', 'test@example.com', '$2b$12$1234567890123456789012', FALSE, 'This is a test user bio'),
(2, 'Reply User', 'reply@example.com', '$2b$12$0987654321098765432109', FALSE, 'Reply user bio'),
(3, 'Admin User', 'admin@example.com', '$2b$12$abcdefghijklmnopqrstuv', TRUE, 'Admin user bio');

-- Insert forum categories through forum_threads
INSERT INTO public.forum_threads (id, user_id, title, content, created_at, category) VALUES
(1, 1, 'Test Thread', 'This is a test thread content', '2025-04-30 12:00:00', 'General'),
(2, 2, 'Another Thread', 'Content of another thread', '2025-04-29 15:30:00', 'Questions'),
(3, 1, 'Announcement Thread', 'Important announcement content', '2025-04-28 09:15:00', 'Announcements'),
(4, 3, 'Admin Thread', 'Thread created by admin', '2025-04-27 14:45:00', 'General');

-- Insert forum replies
INSERT INTO public.forum_replies (id, thread_id, user_id, content, parent_id, created_at, is_edited) VALUES
(1, 1, 2, 'This is a reply to the test thread', NULL, '2025-04-30 12:30:00', FALSE),
(2, 1, 1, 'This is another reply', NULL, '2025-04-30 13:00:00', FALSE),
(3, 2, 3, 'Reply to another thread', NULL, '2025-04-29 16:00:00', FALSE),
(4, 1, 2, 'This is a nested reply', 1, '2025-04-30 12:45:00', FALSE),
(5, 1, 1, 'This is a test reply', NULL, '2025-04-30 14:00:00', FALSE);

-- Insert forum references
INSERT INTO public.forum_references (id, item_type, item_id, reference_type, reference_id, name) VALUES
(1, 'thread', 1, 'article', 42, 'Useful Article'),
(2, 'thread', 1, 'book', 15, 'Reference Book'),
(3, 'reply', 1, 'article', 30, 'Supporting Article'),
(4, 'thread', 2, 'website', 10, 'Website Reference'),
(5, 'thread', 1, 'article', 55, 'Another Article');

-- Insert forum reports
INSERT INTO public.forum_reports (id, user_id, item_type, item_id, reason, resolved) VALUES
(1, 2, 'thread', 4, 'Inappropriate content', FALSE),
(2, 1, 'reply', 3, 'Off-topic', FALSE),
(3, 3, 'thread', 2, 'Spam', TRUE),
(4, 2, 'reply', 4, 'Harassment', FALSE);

SELECT setval('public.users_id_seq', (SELECT MAX(id) FROM public.users), true);

-- Update sequence for forum_threads table
SELECT setval('public.forum_threads_id_seq', (SELECT MAX(id) FROM public.forum_threads), true);

-- Update sequence for forum_replies table
SELECT setval('public.forum_replies_id_seq', (SELECT MAX(id) FROM public.forum_replies), true);

-- Update sequence for forum_references table
SELECT setval('public.forum_references_id_seq', (SELECT MAX(id) FROM public.forum_references), true);

-- Update sequence for forum_reports table
SELECT setval('public.forum_reports_id_seq', (SELECT MAX(id) FROM public.forum_reports), true);
