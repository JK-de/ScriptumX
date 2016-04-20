--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: jk; Type: SCHEMA; Schema: -; Owner: jk
--

CREATE SCHEMA jk;


ALTER SCHEMA jk OWNER TO jk;

--
-- Name: schema_all; Type: SCHEMA; Schema: -; Owner: jk
--

CREATE SCHEMA schema_all;


ALTER SCHEMA schema_all OWNER TO jk;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = jk, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: X_appointment; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_appointment" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    time_all timestamp with time zone,
    duration_all interval,
    meeting_point_id integer,
    note_id integer,
    project_id integer NOT NULL
);


ALTER TABLE "X_appointment" OWNER TO jk;

--
-- Name: X_appointment2scene; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_appointment2scene" (
    id integer NOT NULL,
    "time" time without time zone,
    duration interval,
    appointment_id integer NOT NULL,
    scene_id integer NOT NULL
);


ALTER TABLE "X_appointment2scene" OWNER TO jk;

--
-- Name: X_appointment2scene_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_appointment2scene_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_appointment2scene_id_seq" OWNER TO jk;

--
-- Name: X_appointment2scene_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_appointment2scene_id_seq" OWNED BY "X_appointment2scene".id;


--
-- Name: X_appointment_gadgets; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_appointment_gadgets" (
    id integer NOT NULL,
    appointment_id integer NOT NULL,
    gadget_id integer NOT NULL
);


ALTER TABLE "X_appointment_gadgets" OWNER TO jk;

--
-- Name: X_appointment_gadgets_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_appointment_gadgets_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_appointment_gadgets_id_seq" OWNER TO jk;

--
-- Name: X_appointment_gadgets_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_appointment_gadgets_id_seq" OWNED BY "X_appointment_gadgets".id;


--
-- Name: X_appointment_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_appointment_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_appointment_id_seq" OWNER TO jk;

--
-- Name: X_appointment_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_appointment_id_seq" OWNED BY "X_appointment".id;


--
-- Name: X_appointment_persons; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_appointment_persons" (
    id integer NOT NULL,
    appointment_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE "X_appointment_persons" OWNER TO jk;

--
-- Name: X_appointment_persons_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_appointment_persons_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_appointment_persons_id_seq" OWNER TO jk;

--
-- Name: X_appointment_persons_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_appointment_persons_id_seq" OWNED BY "X_appointment_persons".id;


--
-- Name: X_audio; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_audio" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    progress smallint NOT NULL,
    note_id integer,
    project_id integer NOT NULL,
    CONSTRAINT "X_audio_progress_check" CHECK ((progress >= 0))
);


ALTER TABLE "X_audio" OWNER TO jk;

--
-- Name: X_audio_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_audio_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_audio_id_seq" OWNER TO jk;

--
-- Name: X_audio_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_audio_id_seq" OWNED BY "X_audio".id;


--
-- Name: X_gadget; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_gadget" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    progress smallint NOT NULL,
    note_id integer,
    project_id integer NOT NULL,
    pervasive boolean NOT NULL,
    CONSTRAINT "X_gadget_progress_check" CHECK ((progress >= 0))
);


ALTER TABLE "X_gadget" OWNER TO jk;

--
-- Name: X_gadget_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_gadget_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_gadget_id_seq" OWNER TO jk;

--
-- Name: X_gadget_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_gadget_id_seq" OWNED BY "X_gadget".id;


--
-- Name: X_location; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_location" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    note_id integer,
    project_id integer NOT NULL
);


ALTER TABLE "X_location" OWNER TO jk;

--
-- Name: X_location_gadgets; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_location_gadgets" (
    id integer NOT NULL,
    location_id integer NOT NULL,
    gadget_id integer NOT NULL
);


ALTER TABLE "X_location_gadgets" OWNER TO jk;

--
-- Name: X_location_gadgets_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_location_gadgets_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_location_gadgets_id_seq" OWNER TO jk;

--
-- Name: X_location_gadgets_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_location_gadgets_id_seq" OWNED BY "X_location_gadgets".id;


--
-- Name: X_location_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_location_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_location_id_seq" OWNER TO jk;

--
-- Name: X_location_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_location_id_seq" OWNED BY "X_location".id;


--
-- Name: X_location_persons; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_location_persons" (
    id integer NOT NULL,
    location_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE "X_location_persons" OWNER TO jk;

--
-- Name: X_location_persons_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_location_persons_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_location_persons_id_seq" OWNER TO jk;

--
-- Name: X_location_persons_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_location_persons_id_seq" OWNED BY "X_location_persons".id;


--
-- Name: X_note; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_note" (
    id integer NOT NULL,
    text text NOT NULL,
    created timestamp with time zone NOT NULL,
    author_id integer,
    project_id integer NOT NULL
);


ALTER TABLE "X_note" OWNER TO jk;

--
-- Name: X_note_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_note_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_note_id_seq" OWNER TO jk;

--
-- Name: X_note_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_note_id_seq" OWNED BY "X_note".id;


--
-- Name: X_person; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_person" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    contact text NOT NULL,
    email character varying(254) NOT NULL,
    note_id integer,
    project_id integer NOT NULL,
    pervasive boolean NOT NULL
);


ALTER TABLE "X_person" OWNER TO jk;

--
-- Name: X_person_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_person_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_person_id_seq" OWNER TO jk;

--
-- Name: X_person_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_person_id_seq" OWNED BY "X_person".id;


--
-- Name: X_project; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_project" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE "X_project" OWNER TO jk;

--
-- Name: X_project_guests; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_project_guests" (
    id integer NOT NULL,
    project_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE "X_project_guests" OWNER TO jk;

--
-- Name: X_project_guests_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_project_guests_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_project_guests_id_seq" OWNER TO jk;

--
-- Name: X_project_guests_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_project_guests_id_seq" OWNED BY "X_project_guests".id;


--
-- Name: X_project_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_project_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_project_id_seq" OWNER TO jk;

--
-- Name: X_project_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_project_id_seq" OWNED BY "X_project".id;


--
-- Name: X_project_users; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_project_users" (
    id integer NOT NULL,
    project_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE "X_project_users" OWNER TO jk;

--
-- Name: X_project_users_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_project_users_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_project_users_id_seq" OWNER TO jk;

--
-- Name: X_project_users_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_project_users_id_seq" OWNED BY "X_project_users".id;


--
-- Name: X_role; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_role" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    color character varying(10) NOT NULL,
    actor_id integer,
    note_id integer,
    project_id integer NOT NULL
);


ALTER TABLE "X_role" OWNER TO jk;

--
-- Name: X_role_gadgets; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_role_gadgets" (
    id integer NOT NULL,
    role_id integer NOT NULL,
    gadget_id integer NOT NULL
);


ALTER TABLE "X_role_gadgets" OWNER TO jk;

--
-- Name: X_role_gadgets_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_role_gadgets_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_role_gadgets_id_seq" OWNER TO jk;

--
-- Name: X_role_gadgets_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_role_gadgets_id_seq" OWNED BY "X_role_gadgets".id;


--
-- Name: X_role_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_role_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_role_id_seq" OWNER TO jk;

--
-- Name: X_role_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_role_id_seq" OWNED BY "X_role".id;


--
-- Name: X_scene; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_scene" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    "order" integer NOT NULL,
    short character varying(5) NOT NULL,
    abstract text NOT NULL,
    indentation integer NOT NULL,
    color character varying(10),
    duration interval,
    progress_script smallint NOT NULL,
    progress_pre smallint NOT NULL,
    progress_shot smallint NOT NULL,
    progress_post smallint NOT NULL,
    note_id integer,
    project_id integer NOT NULL,
    script_id integer NOT NULL,
    set_location_id integer,
    CONSTRAINT "X_scene_indentation_check" CHECK ((indentation >= 0)),
    CONSTRAINT "X_scene_order_check" CHECK (("order" >= 0)),
    CONSTRAINT "X_scene_progress_post_check" CHECK ((progress_post >= 0)),
    CONSTRAINT "X_scene_progress_pre_check" CHECK ((progress_pre >= 0)),
    CONSTRAINT "X_scene_progress_script_check" CHECK ((progress_script >= 0)),
    CONSTRAINT "X_scene_progress_shot_check" CHECK ((progress_shot >= 0))
);


ALTER TABLE "X_scene" OWNER TO jk;

--
-- Name: X_scene_audios; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_scene_audios" (
    id integer NOT NULL,
    scene_id integer NOT NULL,
    audio_id integer NOT NULL
);


ALTER TABLE "X_scene_audios" OWNER TO jk;

--
-- Name: X_scene_audios_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_scene_audios_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_scene_audios_id_seq" OWNER TO jk;

--
-- Name: X_scene_audios_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_scene_audios_id_seq" OWNED BY "X_scene_audios".id;


--
-- Name: X_scene_gadgets; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_scene_gadgets" (
    id integer NOT NULL,
    scene_id integer NOT NULL,
    gadget_id integer NOT NULL
);


ALTER TABLE "X_scene_gadgets" OWNER TO jk;

--
-- Name: X_scene_gadgets_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_scene_gadgets_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_scene_gadgets_id_seq" OWNER TO jk;

--
-- Name: X_scene_gadgets_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_scene_gadgets_id_seq" OWNED BY "X_scene_gadgets".id;


--
-- Name: X_scene_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_scene_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_scene_id_seq" OWNER TO jk;

--
-- Name: X_scene_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_scene_id_seq" OWNED BY "X_scene".id;


--
-- Name: X_scene_persons; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_scene_persons" (
    id integer NOT NULL,
    scene_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE "X_scene_persons" OWNER TO jk;

--
-- Name: X_scene_persons_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_scene_persons_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_scene_persons_id_seq" OWNER TO jk;

--
-- Name: X_scene_persons_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_scene_persons_id_seq" OWNED BY "X_scene_persons".id;


--
-- Name: X_scene_sfxs; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_scene_sfxs" (
    id integer NOT NULL,
    scene_id integer NOT NULL,
    sfx_id integer NOT NULL
);


ALTER TABLE "X_scene_sfxs" OWNER TO jk;

--
-- Name: X_scene_sfxs_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_scene_sfxs_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_scene_sfxs_id_seq" OWNER TO jk;

--
-- Name: X_scene_sfxs_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_scene_sfxs_id_seq" OWNED BY "X_scene_sfxs".id;


--
-- Name: X_sceneitem; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_sceneitem" (
    id integer NOT NULL,
    "order" integer NOT NULL,
    type character varying(1) NOT NULL,
    parenthetical character varying(100) NOT NULL,
    text text NOT NULL,
    role_id integer,
    scene_id integer,
    CONSTRAINT "X_sceneitem_order_check" CHECK (("order" >= 0))
);


ALTER TABLE "X_sceneitem" OWNER TO jk;

--
-- Name: X_sceneitem_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_sceneitem_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_sceneitem_id_seq" OWNER TO jk;

--
-- Name: X_sceneitem_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_sceneitem_id_seq" OWNED BY "X_sceneitem".id;


--
-- Name: X_script; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_script" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    abstract text NOT NULL,
    description text NOT NULL,
    author character varying(300) NOT NULL,
    version character varying(50) NOT NULL,
    copyright character varying(300) NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE "X_script" OWNER TO jk;

--
-- Name: X_script_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_script_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_script_id_seq" OWNER TO jk;

--
-- Name: X_script_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_script_id_seq" OWNED BY "X_script".id;


--
-- Name: X_script_persons; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_script_persons" (
    id integer NOT NULL,
    script_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE "X_script_persons" OWNER TO jk;

--
-- Name: X_script_persons_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_script_persons_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_script_persons_id_seq" OWNER TO jk;

--
-- Name: X_script_persons_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_script_persons_id_seq" OWNED BY "X_script_persons".id;


--
-- Name: X_sfx; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE "X_sfx" (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description text NOT NULL,
    tag1 boolean NOT NULL,
    tag2 boolean NOT NULL,
    tag3 boolean NOT NULL,
    tag4 boolean NOT NULL,
    tag5 boolean NOT NULL,
    tag6 boolean NOT NULL,
    tag7 boolean NOT NULL,
    tag8 boolean NOT NULL,
    tag9 boolean NOT NULL,
    tag10 boolean NOT NULL,
    tag11 boolean NOT NULL,
    tag12 boolean NOT NULL,
    progress smallint NOT NULL,
    note_id integer,
    project_id integer NOT NULL,
    CONSTRAINT "X_sfx_progress_check" CHECK ((progress >= 0))
);


ALTER TABLE "X_sfx" OWNER TO jk;

--
-- Name: X_sfx_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE "X_sfx_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "X_sfx_id_seq" OWNER TO jk;

--
-- Name: X_sfx_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE "X_sfx_id_seq" OWNED BY "X_sfx".id;


--
-- Name: auth_group; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO jk;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO jk;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO jk;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO jk;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO jk;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO jk;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO jk;

--
-- Name: auth_user_groups; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO jk;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO jk;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO jk;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO jk;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO jk;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO jk;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO jk;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO jk;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO jk;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO jk;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO jk;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO jk;

--
-- Name: django_site; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO jk;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: jk; Owner: jk
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO jk;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: jk; Owner: jk
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: test; Type: TABLE; Schema: jk; Owner: jk; Tablespace: 
--

CREATE TABLE test (
    id integer NOT NULL
);


ALTER TABLE test OWNER TO jk;

--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment" ALTER COLUMN id SET DEFAULT nextval('"X_appointment_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment2scene" ALTER COLUMN id SET DEFAULT nextval('"X_appointment2scene_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_gadgets" ALTER COLUMN id SET DEFAULT nextval('"X_appointment_gadgets_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_persons" ALTER COLUMN id SET DEFAULT nextval('"X_appointment_persons_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_audio" ALTER COLUMN id SET DEFAULT nextval('"X_audio_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_gadget" ALTER COLUMN id SET DEFAULT nextval('"X_gadget_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location" ALTER COLUMN id SET DEFAULT nextval('"X_location_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_gadgets" ALTER COLUMN id SET DEFAULT nextval('"X_location_gadgets_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_persons" ALTER COLUMN id SET DEFAULT nextval('"X_location_persons_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_note" ALTER COLUMN id SET DEFAULT nextval('"X_note_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_person" ALTER COLUMN id SET DEFAULT nextval('"X_person_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project" ALTER COLUMN id SET DEFAULT nextval('"X_project_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_guests" ALTER COLUMN id SET DEFAULT nextval('"X_project_guests_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_users" ALTER COLUMN id SET DEFAULT nextval('"X_project_users_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role" ALTER COLUMN id SET DEFAULT nextval('"X_role_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role_gadgets" ALTER COLUMN id SET DEFAULT nextval('"X_role_gadgets_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene" ALTER COLUMN id SET DEFAULT nextval('"X_scene_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_audios" ALTER COLUMN id SET DEFAULT nextval('"X_scene_audios_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_gadgets" ALTER COLUMN id SET DEFAULT nextval('"X_scene_gadgets_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_persons" ALTER COLUMN id SET DEFAULT nextval('"X_scene_persons_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_sfxs" ALTER COLUMN id SET DEFAULT nextval('"X_scene_sfxs_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sceneitem" ALTER COLUMN id SET DEFAULT nextval('"X_sceneitem_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_script" ALTER COLUMN id SET DEFAULT nextval('"X_script_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_script_persons" ALTER COLUMN id SET DEFAULT nextval('"X_script_persons_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sfx" ALTER COLUMN id SET DEFAULT nextval('"X_sfx_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: X_appointment2scene_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment2scene"
    ADD CONSTRAINT "X_appointment2scene_pkey" PRIMARY KEY (id);


--
-- Name: X_appointment_gadgets_appointment_id_6c2ac1b0_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment_gadgets"
    ADD CONSTRAINT "X_appointment_gadgets_appointment_id_6c2ac1b0_uniq" UNIQUE (appointment_id, gadget_id);


--
-- Name: X_appointment_gadgets_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment_gadgets"
    ADD CONSTRAINT "X_appointment_gadgets_pkey" PRIMARY KEY (id);


--
-- Name: X_appointment_persons_appointment_id_f78ee247_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment_persons"
    ADD CONSTRAINT "X_appointment_persons_appointment_id_f78ee247_uniq" UNIQUE (appointment_id, person_id);


--
-- Name: X_appointment_persons_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment_persons"
    ADD CONSTRAINT "X_appointment_persons_pkey" PRIMARY KEY (id);


--
-- Name: X_appointment_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_appointment"
    ADD CONSTRAINT "X_appointment_pkey" PRIMARY KEY (id);


--
-- Name: X_audio_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_audio"
    ADD CONSTRAINT "X_audio_pkey" PRIMARY KEY (id);


--
-- Name: X_gadget_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_gadget"
    ADD CONSTRAINT "X_gadget_pkey" PRIMARY KEY (id);


--
-- Name: X_location_gadgets_location_id_b3505d27_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_location_gadgets"
    ADD CONSTRAINT "X_location_gadgets_location_id_b3505d27_uniq" UNIQUE (location_id, gadget_id);


--
-- Name: X_location_gadgets_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_location_gadgets"
    ADD CONSTRAINT "X_location_gadgets_pkey" PRIMARY KEY (id);


--
-- Name: X_location_persons_location_id_6b186712_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_location_persons"
    ADD CONSTRAINT "X_location_persons_location_id_6b186712_uniq" UNIQUE (location_id, person_id);


--
-- Name: X_location_persons_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_location_persons"
    ADD CONSTRAINT "X_location_persons_pkey" PRIMARY KEY (id);


--
-- Name: X_location_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_location"
    ADD CONSTRAINT "X_location_pkey" PRIMARY KEY (id);


--
-- Name: X_note_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_note"
    ADD CONSTRAINT "X_note_pkey" PRIMARY KEY (id);


--
-- Name: X_person_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_person"
    ADD CONSTRAINT "X_person_pkey" PRIMARY KEY (id);


--
-- Name: X_project_guests_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_project_guests"
    ADD CONSTRAINT "X_project_guests_pkey" PRIMARY KEY (id);


--
-- Name: X_project_guests_project_id_e6430c8a_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_project_guests"
    ADD CONSTRAINT "X_project_guests_project_id_e6430c8a_uniq" UNIQUE (project_id, user_id);


--
-- Name: X_project_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_project"
    ADD CONSTRAINT "X_project_pkey" PRIMARY KEY (id);


--
-- Name: X_project_users_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_project_users"
    ADD CONSTRAINT "X_project_users_pkey" PRIMARY KEY (id);


--
-- Name: X_project_users_project_id_f1d8e575_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_project_users"
    ADD CONSTRAINT "X_project_users_project_id_f1d8e575_uniq" UNIQUE (project_id, user_id);


--
-- Name: X_role_gadgets_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_role_gadgets"
    ADD CONSTRAINT "X_role_gadgets_pkey" PRIMARY KEY (id);


--
-- Name: X_role_gadgets_role_id_ba7d19cc_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_role_gadgets"
    ADD CONSTRAINT "X_role_gadgets_role_id_ba7d19cc_uniq" UNIQUE (role_id, gadget_id);


--
-- Name: X_role_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_role"
    ADD CONSTRAINT "X_role_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_audios_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_audios"
    ADD CONSTRAINT "X_scene_audios_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_audios_scene_id_49701f8b_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_audios"
    ADD CONSTRAINT "X_scene_audios_scene_id_49701f8b_uniq" UNIQUE (scene_id, audio_id);


--
-- Name: X_scene_gadgets_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_gadgets"
    ADD CONSTRAINT "X_scene_gadgets_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_gadgets_scene_id_3f92fade_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_gadgets"
    ADD CONSTRAINT "X_scene_gadgets_scene_id_3f92fade_uniq" UNIQUE (scene_id, gadget_id);


--
-- Name: X_scene_persons_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_persons"
    ADD CONSTRAINT "X_scene_persons_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_persons_scene_id_37129480_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_persons"
    ADD CONSTRAINT "X_scene_persons_scene_id_37129480_uniq" UNIQUE (scene_id, person_id);


--
-- Name: X_scene_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene"
    ADD CONSTRAINT "X_scene_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_sfxs_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_sfxs"
    ADD CONSTRAINT "X_scene_sfxs_pkey" PRIMARY KEY (id);


--
-- Name: X_scene_sfxs_scene_id_a0c3fb4b_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_scene_sfxs"
    ADD CONSTRAINT "X_scene_sfxs_scene_id_a0c3fb4b_uniq" UNIQUE (scene_id, sfx_id);


--
-- Name: X_sceneitem_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_sceneitem"
    ADD CONSTRAINT "X_sceneitem_pkey" PRIMARY KEY (id);


--
-- Name: X_script_persons_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_script_persons"
    ADD CONSTRAINT "X_script_persons_pkey" PRIMARY KEY (id);


--
-- Name: X_script_persons_script_id_aef98ab2_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_script_persons"
    ADD CONSTRAINT "X_script_persons_script_id_aef98ab2_uniq" UNIQUE (script_id, person_id);


--
-- Name: X_script_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_script"
    ADD CONSTRAINT "X_script_pkey" PRIMARY KEY (id);


--
-- Name: X_sfx_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY "X_sfx"
    ADD CONSTRAINT "X_sfx_pkey" PRIMARY KEY (id);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: test_pkey; Type: CONSTRAINT; Schema: jk; Owner: jk; Tablespace: 
--

ALTER TABLE ONLY test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- Name: X_appointment2scene_54c91d3b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment2scene_54c91d3b" ON "X_appointment2scene" USING btree (appointment_id);


--
-- Name: X_appointment2scene_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment2scene_c34350a7" ON "X_appointment2scene" USING btree (scene_id);


--
-- Name: X_appointment_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_2115813b" ON "X_appointment" USING btree (note_id);


--
-- Name: X_appointment_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_b098ad43" ON "X_appointment" USING btree (project_id);


--
-- Name: X_appointment_cbaff9c2; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_cbaff9c2" ON "X_appointment" USING btree (meeting_point_id);


--
-- Name: X_appointment_gadgets_54c91d3b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_gadgets_54c91d3b" ON "X_appointment_gadgets" USING btree (appointment_id);


--
-- Name: X_appointment_gadgets_6b81b94a; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_gadgets_6b81b94a" ON "X_appointment_gadgets" USING btree (gadget_id);


--
-- Name: X_appointment_persons_54c91d3b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_persons_54c91d3b" ON "X_appointment_persons" USING btree (appointment_id);


--
-- Name: X_appointment_persons_a8452ca7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_appointment_persons_a8452ca7" ON "X_appointment_persons" USING btree (person_id);


--
-- Name: X_audio_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_audio_2115813b" ON "X_audio" USING btree (note_id);


--
-- Name: X_audio_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_audio_b098ad43" ON "X_audio" USING btree (project_id);


--
-- Name: X_gadget_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_gadget_2115813b" ON "X_gadget" USING btree (note_id);


--
-- Name: X_gadget_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_gadget_b098ad43" ON "X_gadget" USING btree (project_id);


--
-- Name: X_location_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_2115813b" ON "X_location" USING btree (note_id);


--
-- Name: X_location_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_b098ad43" ON "X_location" USING btree (project_id);


--
-- Name: X_location_gadgets_6b81b94a; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_gadgets_6b81b94a" ON "X_location_gadgets" USING btree (gadget_id);


--
-- Name: X_location_gadgets_e274a5da; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_gadgets_e274a5da" ON "X_location_gadgets" USING btree (location_id);


--
-- Name: X_location_persons_a8452ca7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_persons_a8452ca7" ON "X_location_persons" USING btree (person_id);


--
-- Name: X_location_persons_e274a5da; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_location_persons_e274a5da" ON "X_location_persons" USING btree (location_id);


--
-- Name: X_note_4f331e2f; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_note_4f331e2f" ON "X_note" USING btree (author_id);


--
-- Name: X_note_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_note_b098ad43" ON "X_note" USING btree (project_id);


--
-- Name: X_person_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_person_2115813b" ON "X_person" USING btree (note_id);


--
-- Name: X_person_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_person_b098ad43" ON "X_person" USING btree (project_id);


--
-- Name: X_project_5e7b1936; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_project_5e7b1936" ON "X_project" USING btree (owner_id);


--
-- Name: X_project_guests_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_project_guests_b098ad43" ON "X_project_guests" USING btree (project_id);


--
-- Name: X_project_guests_e8701ad4; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_project_guests_e8701ad4" ON "X_project_guests" USING btree (user_id);


--
-- Name: X_project_users_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_project_users_b098ad43" ON "X_project_users" USING btree (project_id);


--
-- Name: X_project_users_e8701ad4; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_project_users_e8701ad4" ON "X_project_users" USING btree (user_id);


--
-- Name: X_role_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_role_2115813b" ON "X_role" USING btree (note_id);


--
-- Name: X_role_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_role_b098ad43" ON "X_role" USING btree (project_id);


--
-- Name: X_role_b39fef6a; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_role_b39fef6a" ON "X_role" USING btree (actor_id);


--
-- Name: X_role_gadgets_6b81b94a; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_role_gadgets_6b81b94a" ON "X_role_gadgets" USING btree (gadget_id);


--
-- Name: X_role_gadgets_84566833; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_role_gadgets_84566833" ON "X_role_gadgets" USING btree (role_id);


--
-- Name: X_scene_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_2115813b" ON "X_scene" USING btree (note_id);


--
-- Name: X_scene_a19ff0c0; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_a19ff0c0" ON "X_scene" USING btree (script_id);


--
-- Name: X_scene_audios_26f6023f; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_audios_26f6023f" ON "X_scene_audios" USING btree (audio_id);


--
-- Name: X_scene_audios_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_audios_c34350a7" ON "X_scene_audios" USING btree (scene_id);


--
-- Name: X_scene_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_b098ad43" ON "X_scene" USING btree (project_id);


--
-- Name: X_scene_c9c59f98; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_c9c59f98" ON "X_scene" USING btree (set_location_id);


--
-- Name: X_scene_gadgets_6b81b94a; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_gadgets_6b81b94a" ON "X_scene_gadgets" USING btree (gadget_id);


--
-- Name: X_scene_gadgets_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_gadgets_c34350a7" ON "X_scene_gadgets" USING btree (scene_id);


--
-- Name: X_scene_persons_a8452ca7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_persons_a8452ca7" ON "X_scene_persons" USING btree (person_id);


--
-- Name: X_scene_persons_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_persons_c34350a7" ON "X_scene_persons" USING btree (scene_id);


--
-- Name: X_scene_sfxs_5f8ea551; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_sfxs_5f8ea551" ON "X_scene_sfxs" USING btree (sfx_id);


--
-- Name: X_scene_sfxs_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_scene_sfxs_c34350a7" ON "X_scene_sfxs" USING btree (scene_id);


--
-- Name: X_sceneitem_84566833; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_sceneitem_84566833" ON "X_sceneitem" USING btree (role_id);


--
-- Name: X_sceneitem_c34350a7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_sceneitem_c34350a7" ON "X_sceneitem" USING btree (scene_id);


--
-- Name: X_script_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_script_b098ad43" ON "X_script" USING btree (project_id);


--
-- Name: X_script_persons_a19ff0c0; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_script_persons_a19ff0c0" ON "X_script_persons" USING btree (script_id);


--
-- Name: X_script_persons_a8452ca7; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_script_persons_a8452ca7" ON "X_script_persons" USING btree (person_id);


--
-- Name: X_sfx_2115813b; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_sfx_2115813b" ON "X_sfx" USING btree (note_id);


--
-- Name: X_sfx_b098ad43; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX "X_sfx_b098ad43" ON "X_sfx" USING btree (project_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: jk; Owner: jk; Tablespace: 
--

CREATE INDEX django_site_domain_a2e37b91_like ON django_site USING btree (domain varchar_pattern_ops);


--
-- Name: X_appointment2scene_appointment_id_eab464b6_fk_X_appointment_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment2scene"
    ADD CONSTRAINT "X_appointment2scene_appointment_id_eab464b6_fk_X_appointment_id" FOREIGN KEY (appointment_id) REFERENCES "X_appointment"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment2scene_scene_id_316f7152_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment2scene"
    ADD CONSTRAINT "X_appointment2scene_scene_id_316f7152_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_gadge_appointment_id_e2370c58_fk_X_appointment_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_gadgets"
    ADD CONSTRAINT "X_appointment_gadge_appointment_id_e2370c58_fk_X_appointment_id" FOREIGN KEY (appointment_id) REFERENCES "X_appointment"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_gadgets_gadget_id_2c60d288_fk_X_gadget_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_gadgets"
    ADD CONSTRAINT "X_appointment_gadgets_gadget_id_2c60d288_fk_X_gadget_id" FOREIGN KEY (gadget_id) REFERENCES "X_gadget"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_meeting_point_id_8b3965d0_fk_X_location_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment"
    ADD CONSTRAINT "X_appointment_meeting_point_id_8b3965d0_fk_X_location_id" FOREIGN KEY (meeting_point_id) REFERENCES "X_location"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_note_id_b01a1e83_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment"
    ADD CONSTRAINT "X_appointment_note_id_b01a1e83_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_perso_appointment_id_6e7f0e66_fk_X_appointment_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_persons"
    ADD CONSTRAINT "X_appointment_perso_appointment_id_6e7f0e66_fk_X_appointment_id" FOREIGN KEY (appointment_id) REFERENCES "X_appointment"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_persons_person_id_d47b0165_fk_X_person_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment_persons"
    ADD CONSTRAINT "X_appointment_persons_person_id_d47b0165_fk_X_person_id" FOREIGN KEY (person_id) REFERENCES "X_person"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_appointment_project_id_629d08ec_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_appointment"
    ADD CONSTRAINT "X_appointment_project_id_629d08ec_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_audio_note_id_e6c0e276_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_audio"
    ADD CONSTRAINT "X_audio_note_id_e6c0e276_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_audio_project_id_96d3b04b_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_audio"
    ADD CONSTRAINT "X_audio_project_id_96d3b04b_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_gadget_note_id_841b6ad0_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_gadget"
    ADD CONSTRAINT "X_gadget_note_id_841b6ad0_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_gadget_project_id_851fc3f4_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_gadget"
    ADD CONSTRAINT "X_gadget_project_id_851fc3f4_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_gadgets_gadget_id_741e84be_fk_X_gadget_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_gadgets"
    ADD CONSTRAINT "X_location_gadgets_gadget_id_741e84be_fk_X_gadget_id" FOREIGN KEY (gadget_id) REFERENCES "X_gadget"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_gadgets_location_id_a60ebdbe_fk_X_location_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_gadgets"
    ADD CONSTRAINT "X_location_gadgets_location_id_a60ebdbe_fk_X_location_id" FOREIGN KEY (location_id) REFERENCES "X_location"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_note_id_780cb953_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location"
    ADD CONSTRAINT "X_location_note_id_780cb953_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_persons_location_id_4cdf1aa9_fk_X_location_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_persons"
    ADD CONSTRAINT "X_location_persons_location_id_4cdf1aa9_fk_X_location_id" FOREIGN KEY (location_id) REFERENCES "X_location"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_persons_person_id_548df6f0_fk_X_person_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location_persons"
    ADD CONSTRAINT "X_location_persons_person_id_548df6f0_fk_X_person_id" FOREIGN KEY (person_id) REFERENCES "X_person"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_location_project_id_cb8c2169_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_location"
    ADD CONSTRAINT "X_location_project_id_cb8c2169_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_note_author_id_3e3e82a3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_note"
    ADD CONSTRAINT "X_note_author_id_3e3e82a3_fk_auth_user_id" FOREIGN KEY (author_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_note_project_id_dbba9b0c_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_note"
    ADD CONSTRAINT "X_note_project_id_dbba9b0c_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_person_note_id_22462bed_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_person"
    ADD CONSTRAINT "X_person_note_id_22462bed_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_person_project_id_2d8f7b17_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_person"
    ADD CONSTRAINT "X_person_project_id_2d8f7b17_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_project_guests_project_id_c1934793_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_guests"
    ADD CONSTRAINT "X_project_guests_project_id_c1934793_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_project_guests_user_id_72073746_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_guests"
    ADD CONSTRAINT "X_project_guests_user_id_72073746_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_project_owner_id_a1a507ba_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project"
    ADD CONSTRAINT "X_project_owner_id_a1a507ba_fk_auth_user_id" FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_project_users_project_id_45942cd9_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_users"
    ADD CONSTRAINT "X_project_users_project_id_45942cd9_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_project_users_user_id_90294a0a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_project_users"
    ADD CONSTRAINT "X_project_users_user_id_90294a0a_fk_auth_user_id" FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_role_actor_id_82dccdbf_fk_X_person_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role"
    ADD CONSTRAINT "X_role_actor_id_82dccdbf_fk_X_person_id" FOREIGN KEY (actor_id) REFERENCES "X_person"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_role_gadgets_gadget_id_09274af0_fk_X_gadget_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role_gadgets"
    ADD CONSTRAINT "X_role_gadgets_gadget_id_09274af0_fk_X_gadget_id" FOREIGN KEY (gadget_id) REFERENCES "X_gadget"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_role_gadgets_role_id_fd266c8f_fk_X_role_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role_gadgets"
    ADD CONSTRAINT "X_role_gadgets_role_id_fd266c8f_fk_X_role_id" FOREIGN KEY (role_id) REFERENCES "X_role"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_role_note_id_21451800_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role"
    ADD CONSTRAINT "X_role_note_id_21451800_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_role_project_id_0118ca9f_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_role"
    ADD CONSTRAINT "X_role_project_id_0118ca9f_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_audios_audio_id_f2382049_fk_X_audio_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_audios"
    ADD CONSTRAINT "X_scene_audios_audio_id_f2382049_fk_X_audio_id" FOREIGN KEY (audio_id) REFERENCES "X_audio"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_audios_scene_id_226473ef_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_audios"
    ADD CONSTRAINT "X_scene_audios_scene_id_226473ef_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_gadgets_gadget_id_43852dc7_fk_X_gadget_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_gadgets"
    ADD CONSTRAINT "X_scene_gadgets_gadget_id_43852dc7_fk_X_gadget_id" FOREIGN KEY (gadget_id) REFERENCES "X_gadget"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_gadgets_scene_id_5a431e76_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_gadgets"
    ADD CONSTRAINT "X_scene_gadgets_scene_id_5a431e76_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_note_id_4a61a9c8_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene"
    ADD CONSTRAINT "X_scene_note_id_4a61a9c8_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_persons_person_id_1d74b09b_fk_X_person_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_persons"
    ADD CONSTRAINT "X_scene_persons_person_id_1d74b09b_fk_X_person_id" FOREIGN KEY (person_id) REFERENCES "X_person"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_persons_scene_id_d7cc1112_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_persons"
    ADD CONSTRAINT "X_scene_persons_scene_id_d7cc1112_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_project_id_9df36424_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene"
    ADD CONSTRAINT "X_scene_project_id_9df36424_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_script_id_b0801646_fk_X_script_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene"
    ADD CONSTRAINT "X_scene_script_id_b0801646_fk_X_script_id" FOREIGN KEY (script_id) REFERENCES "X_script"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_set_location_id_8e5f5d46_fk_X_location_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene"
    ADD CONSTRAINT "X_scene_set_location_id_8e5f5d46_fk_X_location_id" FOREIGN KEY (set_location_id) REFERENCES "X_location"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_sfxs_scene_id_b48bd0d3_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_sfxs"
    ADD CONSTRAINT "X_scene_sfxs_scene_id_b48bd0d3_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_scene_sfxs_sfx_id_c37cd631_fk_X_sfx_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_scene_sfxs"
    ADD CONSTRAINT "X_scene_sfxs_sfx_id_c37cd631_fk_X_sfx_id" FOREIGN KEY (sfx_id) REFERENCES "X_sfx"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_sceneitem_role_id_7ca7575e_fk_X_role_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sceneitem"
    ADD CONSTRAINT "X_sceneitem_role_id_7ca7575e_fk_X_role_id" FOREIGN KEY (role_id) REFERENCES "X_role"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_sceneitem_scene_id_5b3398aa_fk_X_scene_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sceneitem"
    ADD CONSTRAINT "X_sceneitem_scene_id_5b3398aa_fk_X_scene_id" FOREIGN KEY (scene_id) REFERENCES "X_scene"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_script_persons_person_id_de5516ba_fk_X_person_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_script_persons"
    ADD CONSTRAINT "X_script_persons_person_id_de5516ba_fk_X_person_id" FOREIGN KEY (person_id) REFERENCES "X_person"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_script_persons_script_id_e49fa3e2_fk_X_script_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_script_persons"
    ADD CONSTRAINT "X_script_persons_script_id_e49fa3e2_fk_X_script_id" FOREIGN KEY (script_id) REFERENCES "X_script"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_script_project_id_1b0101f5_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_script"
    ADD CONSTRAINT "X_script_project_id_1b0101f5_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_sfx_note_id_1f268537_fk_X_note_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sfx"
    ADD CONSTRAINT "X_sfx_note_id_1f268537_fk_X_note_id" FOREIGN KEY (note_id) REFERENCES "X_note"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: X_sfx_project_id_9a72f4f2_fk_X_project_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY "X_sfx"
    ADD CONSTRAINT "X_sfx_project_id_9a72f4f2_fk_X_project_id" FOREIGN KEY (project_id) REFERENCES "X_project"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: jk; Owner: jk
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

