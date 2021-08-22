/*
 Navicat Premium Data Transfer

 Source Server         : Contabo
 Source Server Type    : PostgreSQL
 Source Server Version : 120007
 Source Host           : 144.91.110.3:5432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120007
 File Encoding         : 65001

 Date: 22/08/2021 11:21:00
*/


-- ----------------------------
-- Sequence structure for blackjack_game_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."blackjack_game_id_seq";
CREATE SEQUENCE "public"."blackjack_game_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for deposits_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."deposits_id_seq";
CREATE SEQUENCE "public"."deposits_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for psr_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."psr_id_seq";
CREATE SEQUENCE "public"."psr_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for psr_round_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."psr_round_id_seq";
CREATE SEQUENCE "public"."psr_round_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for rates_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."rates_id_seq";
CREATE SEQUENCE "public"."rates_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for rockpaperscisors_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."rockpaperscisors_id_seq";
CREATE SEQUENCE "public"."rockpaperscisors_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for rooms_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."rooms_id_seq";
CREATE SEQUENCE "public"."rooms_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tiktaktoe_cell_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tiktaktoe_cell_id_seq";
CREATE SEQUENCE "public"."tiktaktoe_cell_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tiktaktoe_game_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tiktaktoe_game_id_seq";
CREATE SEQUENCE "public"."tiktaktoe_game_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for blackjack_game
-- ----------------------------
DROP TABLE IF EXISTS "public"."blackjack_game";
CREATE TABLE "public"."blackjack_game" (
  "id" int4 NOT NULL DEFAULT nextval('blackjack_game_id_seq'::regclass),
  "rates_id" int4,
  "result" varchar(15) COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "game_round" int4 DEFAULT 1,
  "is_end" varchar(10) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of blackjack_game
-- ----------------------------

-- ----------------------------
-- Table structure for blackjack_game_dealer
-- ----------------------------
DROP TABLE IF EXISTS "public"."blackjack_game_dealer";
CREATE TABLE "public"."blackjack_game_dealer" (
  "game_id" int4,
  "deck" json DEFAULT '[]'::json,
  "hand" json DEFAULT '[]'::json
)
;

-- ----------------------------
-- Records of blackjack_game_dealer
-- ----------------------------

-- ----------------------------
-- Table structure for blackjack_game_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."blackjack_game_user";
CREATE TABLE "public"."blackjack_game_user" (
  "user_id" int4,
  "game_id" int4,
  "chat_id" int4,
  "hand" json DEFAULT '[]'::json,
  "state" varchar(10) COLLATE "pg_catalog"."default" DEFAULT 'NONE'::character varying
)
;

-- ----------------------------
-- Records of blackjack_game_user
-- ----------------------------

-- ----------------------------
-- Table structure for blackjack_lobby
-- ----------------------------
DROP TABLE IF EXISTS "public"."blackjack_lobby";
CREATE TABLE "public"."blackjack_lobby" (
  "user_id" int8,
  "rates_id" int4
)
;

-- ----------------------------
-- Records of blackjack_lobby
-- ----------------------------

-- ----------------------------
-- Table structure for deposits
-- ----------------------------
DROP TABLE IF EXISTS "public"."deposits";
CREATE TABLE "public"."deposits" (
  "id" int4 NOT NULL DEFAULT nextval('deposits_id_seq'::regclass),
  "user_id" int4,
  "balance" int4 DEFAULT 0
)
;

-- ----------------------------
-- Records of deposits
-- ----------------------------
INSERT INTO "public"."deposits" VALUES (1, 400717618, 0);
INSERT INTO "public"."deposits" VALUES (2, 462567885, 0);
INSERT INTO "public"."deposits" VALUES (3, 475422085, 0);
INSERT INTO "public"."deposits" VALUES (4, 383492784, 0);
INSERT INTO "public"."deposits" VALUES (5, 573332887, 0);

-- ----------------------------
-- Table structure for psr
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr";
CREATE TABLE "public"."psr" (
  "id" int4 NOT NULL DEFAULT nextval('psr_id_seq'::regclass),
  "rates_id" int4,
  "game_type_id" int4,
  "is_end" bool DEFAULT false,
  "user_count" int4,
  "round_id" int4
)
;

-- ----------------------------
-- Records of psr
-- ----------------------------

-- ----------------------------
-- Table structure for psr_game_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_game_type";
CREATE TABLE "public"."psr_game_type" (
  "id" int8 NOT NULL,
  "title" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of psr_game_type
-- ----------------------------
INSERT INTO "public"."psr_game_type" VALUES (1, 'Default');

-- ----------------------------
-- Table structure for psr_lobby
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_lobby";
CREATE TABLE "public"."psr_lobby" (
  "user_id" int8 NOT NULL,
  "rates_id" int8,
  "user_count" int4
)
;

-- ----------------------------
-- Records of psr_lobby
-- ----------------------------

-- ----------------------------
-- Table structure for psr_round
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_round";
CREATE TABLE "public"."psr_round" (
  "id" int4 NOT NULL DEFAULT nextval('psr_round_id_seq'::regclass),
  "psr_id" int4 NOT NULL,
  "sequence" int4 NOT NULL DEFAULT 1
)
;

-- ----------------------------
-- Records of psr_round
-- ----------------------------

-- ----------------------------
-- Table structure for psr_round_user_variant
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_round_user_variant";
CREATE TABLE "public"."psr_round_user_variant" (
  "round_id" int4 NOT NULL,
  "user_id" int4 NOT NULL,
  "variant_id" int4
)
;

-- ----------------------------
-- Records of psr_round_user_variant
-- ----------------------------

-- ----------------------------
-- Table structure for psr_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_user";
CREATE TABLE "public"."psr_user" (
  "user_id" int8 NOT NULL,
  "psr_id" int4,
  "message_id" int8
)
;

-- ----------------------------
-- Records of psr_user
-- ----------------------------

-- ----------------------------
-- Table structure for psr_variant
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_variant";
CREATE TABLE "public"."psr_variant" (
  "id" int4 NOT NULL,
  "title" text COLLATE "pg_catalog"."default",
  "game_type_id" int4
)
;

-- ----------------------------
-- Records of psr_variant
-- ----------------------------
INSERT INTO "public"."psr_variant" VALUES (1, 'Камень', 1);
INSERT INTO "public"."psr_variant" VALUES (2, 'Ножницы', 1);
INSERT INTO "public"."psr_variant" VALUES (3, 'Бумага', 1);

-- ----------------------------
-- Table structure for psr_variant_beat
-- ----------------------------
DROP TABLE IF EXISTS "public"."psr_variant_beat";
CREATE TABLE "public"."psr_variant_beat" (
  "variant_id" int4 NOT NULL,
  "beat_variant_id" int4 NOT NULL
)
;

-- ----------------------------
-- Records of psr_variant_beat
-- ----------------------------
INSERT INTO "public"."psr_variant_beat" VALUES (1, 2);
INSERT INTO "public"."psr_variant_beat" VALUES (2, 3);
INSERT INTO "public"."psr_variant_beat" VALUES (3, 1);

-- ----------------------------
-- Table structure for rates
-- ----------------------------
DROP TABLE IF EXISTS "public"."rates";
CREATE TABLE "public"."rates" (
  "id" int4 NOT NULL DEFAULT nextval('rates_id_seq'::regclass),
  "value" int4
)
;

-- ----------------------------
-- Records of rates
-- ----------------------------
INSERT INTO "public"."rates" VALUES (1, 5);
INSERT INTO "public"."rates" VALUES (2, 10);

-- ----------------------------
-- Table structure for rockpaperscisors
-- ----------------------------
DROP TABLE IF EXISTS "public"."rockpaperscisors";
CREATE TABLE "public"."rockpaperscisors" (
  "id" int4 NOT NULL DEFAULT nextval('rockpaperscisors_id_seq'::regclass),
  "room_id" int4,
  "choose_player1" text COLLATE "pg_catalog"."default",
  "choose_player2" text COLLATE "pg_catalog"."default",
  "result_player1" text COLLATE "pg_catalog"."default",
  "result_player2" text COLLATE "pg_catalog"."default",
  "id_room_rps" int4,
  "score" int4,
  "answer_player1" int4,
  "answer_player2" int4,
  "winning_answer" text COLLATE "pg_catalog"."default",
  "win_player" bool
)
;

-- ----------------------------
-- Records of rockpaperscisors
-- ----------------------------

-- ----------------------------
-- Table structure for rooms
-- ----------------------------
DROP TABLE IF EXISTS "public"."rooms";
CREATE TABLE "public"."rooms" (
  "id" int4 NOT NULL DEFAULT nextval('rooms_id_seq'::regclass),
  "player_one" int4 NOT NULL,
  "player_two" int4,
  "player_one_ready" bool DEFAULT false,
  "player_two_ready" bool DEFAULT false,
  "timeout" int4 DEFAULT 300,
  "room_state" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 'WAITING'::character varying
)
;

-- ----------------------------
-- Records of rooms
-- ----------------------------

-- ----------------------------
-- Table structure for tiktaktoe_cell
-- ----------------------------
DROP TABLE IF EXISTS "public"."tiktaktoe_cell";
CREATE TABLE "public"."tiktaktoe_cell" (
  "is_busy" bool DEFAULT false,
  "user_id" int8,
  "game_id" int8 NOT NULL,
  "id" int4 NOT NULL DEFAULT nextval('tiktaktoe_cell_id_seq'::regclass)
)
;

-- ----------------------------
-- Records of tiktaktoe_cell
-- ----------------------------
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 461);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 462);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 463);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 464);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 466);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 467);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('f', NULL, 59, 468);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('t', 400717618, 59, 460);
INSERT INTO "public"."tiktaktoe_cell" VALUES ('t', 475422085, 59, 465);

-- ----------------------------
-- Table structure for tiktaktoe_game
-- ----------------------------
DROP TABLE IF EXISTS "public"."tiktaktoe_game";
CREATE TABLE "public"."tiktaktoe_game" (
  "id" int8 NOT NULL DEFAULT nextval('tiktaktoe_game_id_seq'::regclass),
  "rates_id" int4,
  "user_step_id" int8,
  "is_end" bool NOT NULL DEFAULT false,
  "step" int4 NOT NULL DEFAULT 1
)
;

-- ----------------------------
-- Records of tiktaktoe_game
-- ----------------------------
INSERT INTO "public"."tiktaktoe_game" VALUES (59, 1, 400717618, 'f', 3);

-- ----------------------------
-- Table structure for tiktaktoe_game_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."tiktaktoe_game_user";
CREATE TABLE "public"."tiktaktoe_game_user" (
  "user_id" int4 NOT NULL,
  "game_id" int8 NOT NULL,
  "character" text COLLATE "pg_catalog"."default" NOT NULL,
  "message_id" int8
)
;

-- ----------------------------
-- Records of tiktaktoe_game_user
-- ----------------------------
INSERT INTO "public"."tiktaktoe_game_user" VALUES (475422085, 59, 'O', 2926);
INSERT INTO "public"."tiktaktoe_game_user" VALUES (400717618, 59, 'X', 2927);

-- ----------------------------
-- Table structure for tiktaktoe_lobby
-- ----------------------------
DROP TABLE IF EXISTS "public"."tiktaktoe_lobby";
CREATE TABLE "public"."tiktaktoe_lobby" (
  "user_id" int8 NOT NULL,
  "rates_id" int4
)
;

-- ----------------------------
-- Records of tiktaktoe_lobby
-- ----------------------------

-- ----------------------------
-- Table structure for tiktaktoe_user_step
-- ----------------------------
DROP TABLE IF EXISTS "public"."tiktaktoe_user_step";
CREATE TABLE "public"."tiktaktoe_user_step" (
  "game_id" int4 NOT NULL,
  "sequence" int4 NOT NULL,
  "user_id" int4 NOT NULL
)
;

-- ----------------------------
-- Records of tiktaktoe_user_step
-- ----------------------------
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 1, 400717618);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 2, 475422085);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 3, 400717618);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 4, 475422085);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 5, 400717618);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 6, 475422085);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 7, 400717618);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 8, 475422085);
INSERT INTO "public"."tiktaktoe_user_step" VALUES (59, 9, 400717618);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "username" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES (400717618, 'Вова', 'v_zna4it_volodia');
INSERT INTO "public"."users" VALUES (462567885, 'Maxon', 'lux3r');
INSERT INTO "public"."users" VALUES (475422085, 'Оаоао', 'what_i_have_to_do_with_this_shit');
INSERT INTO "public"."users" VALUES (383492784, 'Ｆｏｒｅｖｋａ ÐΞV', 'Forevka');
INSERT INTO "public"."users" VALUES (573332887, 'Порно', 'georeperboleja');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."blackjack_game_id_seq"
OWNED BY "public"."blackjack_game"."id";
SELECT setval('"public"."blackjack_game_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."deposits_id_seq"
OWNED BY "public"."deposits"."id";
SELECT setval('"public"."deposits_id_seq"', 6, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."psr_id_seq"', 8, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."psr_round_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."rates_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."rockpaperscisors_id_seq"
OWNED BY "public"."rockpaperscisors"."id";
SELECT setval('"public"."rockpaperscisors_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."rooms_id_seq"
OWNED BY "public"."rooms"."id";
SELECT setval('"public"."rooms_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."tiktaktoe_cell_id_seq"', 469, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."tiktaktoe_game_id_seq"', 60, true);

-- ----------------------------
-- Primary Key structure for table blackjack_game
-- ----------------------------
ALTER TABLE "public"."blackjack_game" ADD CONSTRAINT "blackjack_game_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table deposits
-- ----------------------------
ALTER TABLE "public"."deposits" ADD CONSTRAINT "deposits_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table psr
-- ----------------------------
ALTER TABLE "public"."psr" ADD CONSTRAINT "psr_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table psr_game_type
-- ----------------------------
ALTER TABLE "public"."psr_game_type" ADD CONSTRAINT "psr_game_type_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table psr_lobby
-- ----------------------------
ALTER TABLE "public"."psr_lobby" ADD CONSTRAINT "psr_lobby_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table psr_round
-- ----------------------------
ALTER TABLE "public"."psr_round" ADD CONSTRAINT "psr_round_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table psr_round_user_variant
-- ----------------------------
ALTER TABLE "public"."psr_round_user_variant" ADD CONSTRAINT "psr_round_user_variant_pkey" PRIMARY KEY ("round_id", "user_id");

-- ----------------------------
-- Primary Key structure for table psr_user
-- ----------------------------
ALTER TABLE "public"."psr_user" ADD CONSTRAINT "psr_user_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table psr_variant
-- ----------------------------
ALTER TABLE "public"."psr_variant" ADD CONSTRAINT "psr_variant_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table psr_variant_beat
-- ----------------------------
ALTER TABLE "public"."psr_variant_beat" ADD CONSTRAINT "psr_variant_beat_pkey" PRIMARY KEY ("variant_id", "beat_variant_id");

-- ----------------------------
-- Primary Key structure for table rates
-- ----------------------------
ALTER TABLE "public"."rates" ADD CONSTRAINT "rates_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table rockpaperscisors
-- ----------------------------
ALTER TABLE "public"."rockpaperscisors" ADD CONSTRAINT "rockpaperscisors_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table rooms
-- ----------------------------
ALTER TABLE "public"."rooms" ADD CONSTRAINT "rooms_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table tiktaktoe_cell
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_cell" ADD CONSTRAINT "tiktaktoe_cell_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table tiktaktoe_game
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_game" ADD CONSTRAINT "tiktaktoe_game_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table tiktaktoe_game_user
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_game_user" ADD CONSTRAINT "tiktaktoe_game_user_pkey" PRIMARY KEY ("user_id", "game_id");

-- ----------------------------
-- Primary Key structure for table tiktaktoe_lobby
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_lobby" ADD CONSTRAINT "tiktaktoe_lobby_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Primary Key structure for table tiktaktoe_user_step
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_user_step" ADD CONSTRAINT "tiktaktoe_user_step_pkey" PRIMARY KEY ("game_id", "sequence", "user_id");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table blackjack_game
-- ----------------------------
ALTER TABLE "public"."blackjack_game" ADD CONSTRAINT "blackjack_game_rates_id_fkey" FOREIGN KEY ("rates_id") REFERENCES "public"."rates" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table blackjack_game_dealer
-- ----------------------------
ALTER TABLE "public"."blackjack_game_dealer" ADD CONSTRAINT "blackjack_game_dealer_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "public"."blackjack_game" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table blackjack_game_user
-- ----------------------------
ALTER TABLE "public"."blackjack_game_user" ADD CONSTRAINT "blackjack_game_user_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "public"."blackjack_game" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."blackjack_game_user" ADD CONSTRAINT "blackjack_game_user_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table blackjack_lobby
-- ----------------------------
ALTER TABLE "public"."blackjack_lobby" ADD CONSTRAINT "blackjack_lobby_rates_id_fkey" FOREIGN KEY ("rates_id") REFERENCES "public"."rates" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."blackjack_lobby" ADD CONSTRAINT "blackjack_lobby_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table deposits
-- ----------------------------
ALTER TABLE "public"."deposits" ADD CONSTRAINT "deposits_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr
-- ----------------------------
ALTER TABLE "public"."psr" ADD CONSTRAINT "psr_game_type_id_fkey" FOREIGN KEY ("game_type_id") REFERENCES "public"."psr" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."psr" ADD CONSTRAINT "psr_rates_id_fkey" FOREIGN KEY ("rates_id") REFERENCES "public"."rates" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."psr" ADD CONSTRAINT "psr_round_id_fkey" FOREIGN KEY ("round_id") REFERENCES "public"."psr_round" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_lobby
-- ----------------------------
ALTER TABLE "public"."psr_lobby" ADD CONSTRAINT "psr_lobby_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_round
-- ----------------------------
ALTER TABLE "public"."psr_round" ADD CONSTRAINT "psr_round_psr_id_fkey" FOREIGN KEY ("psr_id") REFERENCES "public"."psr" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_round_user_variant
-- ----------------------------
ALTER TABLE "public"."psr_round_user_variant" ADD CONSTRAINT "psr_round_user_variant_round_id_fkey" FOREIGN KEY ("round_id") REFERENCES "public"."psr_round" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."psr_round_user_variant" ADD CONSTRAINT "psr_round_user_variant_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_user
-- ----------------------------
ALTER TABLE "public"."psr_user" ADD CONSTRAINT "psr_user_psr_id_fkey" FOREIGN KEY ("psr_id") REFERENCES "public"."psr" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."psr_user" ADD CONSTRAINT "psr_user_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_variant
-- ----------------------------
ALTER TABLE "public"."psr_variant" ADD CONSTRAINT "psr_variant_game_type_id_fkey" FOREIGN KEY ("game_type_id") REFERENCES "public"."psr_game_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table psr_variant_beat
-- ----------------------------
ALTER TABLE "public"."psr_variant_beat" ADD CONSTRAINT "psr_variant_beat_beat_variant_id_fkey" FOREIGN KEY ("beat_variant_id") REFERENCES "public"."psr_variant" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."psr_variant_beat" ADD CONSTRAINT "psr_variant_beat_variant_id_fkey" FOREIGN KEY ("variant_id") REFERENCES "public"."psr_variant" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table rockpaperscisors
-- ----------------------------
ALTER TABLE "public"."rockpaperscisors" ADD CONSTRAINT "rockpaperscisors_room_id_fkey" FOREIGN KEY ("room_id") REFERENCES "public"."rooms" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table rooms
-- ----------------------------
ALTER TABLE "public"."rooms" ADD CONSTRAINT "rooms_player_one_fkey" FOREIGN KEY ("player_one") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."rooms" ADD CONSTRAINT "rooms_player_two_fkey" FOREIGN KEY ("player_two") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table tiktaktoe_cell
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_cell" ADD CONSTRAINT "tiktaktoe_cell_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "public"."tiktaktoe_game" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table tiktaktoe_game
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_game" ADD CONSTRAINT "tiktaktoe_game_rates_id_fkey" FOREIGN KEY ("rates_id") REFERENCES "public"."rates" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."tiktaktoe_game" ADD CONSTRAINT "tiktaktoe_game_user_step_id_fkey" FOREIGN KEY ("user_step_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table tiktaktoe_game_user
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_game_user" ADD CONSTRAINT "tiktaktoe_game_user_tiktaktoe_game_id_fkey" FOREIGN KEY ("game_id") REFERENCES "public"."tiktaktoe_game" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."tiktaktoe_game_user" ADD CONSTRAINT "tiktaktoe_game_user_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table tiktaktoe_lobby
-- ----------------------------
ALTER TABLE "public"."tiktaktoe_lobby" ADD CONSTRAINT "tiktaktoe_lobby_rates_id_fkey" FOREIGN KEY ("rates_id") REFERENCES "public"."rates" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."tiktaktoe_lobby" ADD CONSTRAINT "tiktaktoe_lobby_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
