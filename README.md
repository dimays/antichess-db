# AntichessDB

AntichessDB is a website that allows you to interact with data from Lichess specifically focused on the popular variant Antichess.

## Overview

We are currently on v0.0 of the site. The planned development phases include:

| Version | Description                              | Expected Delivery Date |
| ------- | ---------------------------------------- | ---------------------- |
| v0.0    | Alpha Website Launched with Landing Page | May 12, 2023           |
| v0.1    | Query Builder Launched                   | May 26, 2023           |
| v0.2    | Player Scorecards Launched               | June 16, 2023          |
| v0.3    | Analytics Launched                       | July 14, 2023          |
| v1.0    | General Release                          | July 28, 2023          |

## Data Model

This Entity Relationship Diagram shows how each table relates to the others, as well as a quick reference of field constraints (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `FOREIGN_KEY`).

![AntichessDB ERD](/acdb_app/static/acdb_app/img/ERD.png "AntichessDB ERD")

## Data Dictionary

This data dictionary is foundational to all parts of the app. The records in these tables will be generated from an automated PGN parsing system (TBD) which will allow us to upsert records across the database for games fetched from the Lichess Public Database or from the Lichess API.

### `players` Table

**A record for each player on Lichess who has played at least one rated Antichess game**

| Column Name      | Data Type               | Description                                                                              |
| ---------------- | ----------------------- | ---------------------------------------------------------------------------------------- |
| player_id        | bigint                  | Primary key representing a Lichess user who has played at least one rated Antichess game |
| lichess_username | varchar(30)             | Unique username for this Lichess player (always represented in lowercase)                |
| created_at       | timestamp with timezone | Time (in UTC) at which this record was created                                           |
| updated_at       | timestamp with timezone | Time (in UTC) at which this record was most recently updated                             |
| deleted_at       | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)                  |

### `events` Table

**A record for each Lichess event (Arena or Swiss Tournament) during which at least one rated Antichess game was played**

| Column Name            | Data Type               | Description                                                                                                                                     |
| ---------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| event_id               | bigint                  | Primary key representing a Lichess event                                                                                                        |
| lichess_event_id       | varchar(30)             | Unique, external Lichess ID for this Lichess event, prefixed with 'swiss-' if a Swiss tournament, prefixed with 'arena-' if an Arena tournament |
| event_name             | varchar(30)             | Name for this Lichess event                                                                                                                     |
| start_date_utc         | date                    | Date (in UTC) on which this event began                                                                                                         |
| start_time_utc         | timestamp with timezone | Timestamp (in UTC) at which this event began                                                                                                    |
| duration_minutes       | smallint                | Number of minutes this event lasted                                                                                                             |
| first_place_player_id  | bigint                  | Foreign key, references players.player_id, represents the player that won this event                                                            |
| second_place_player_id | bigint                  | Foreign key, references players.player_id, represents the player that got second place at this event                                            |
| third_place_player_id  | bigint                  | Foreign key, references players.player_id, represents the player that got third place at this event                                             |
| created_at             | timestamp with timezone | Time (in UTC) at which this record was created                                                                                                  |
| updated_at             | timestamp with timezone | Time (in UTC) at which this record was most recently updated                                                                                    |
| deleted_at             | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)                                                                         |

### `positions` Table

**A record for each unique position that has been achieved in at least one rated Antichess game on Lichess**

| Column Name   | Data Type               | Description                                                                                                                                                                                                                                              |
| ------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| position_id   | bigint                  | Primary key representing a unique board position                                                                                                                                                                                                         |
| fen           | varchar(100)            | Representation of this position in abbreviated Forsyth-Edwards Notation (FEN), does not include some fields which are not necessary for the purposes of evaluating the position, such as move number                                                     |
| eval          | varchar(20)             | Formatted string representing a centipawn value (eg. '-1.3') or a forced mate (eg. '#7')                                                                                                                                                                 |
| cp            | decimal(9,1)            | Fairy Stockfish’s centipawn evaluation for this position, with one decimal place (can be NULL if evaluation is a forced mate instead)                                                                                                                    |
| mate          | smallint                | Fairy Stockfish’s evaluation of the minimum number of moves until mate for this position, expressed as a positive if a mate for white, and as a negative if a mate for black (can be NULL if Fairy Stockfish cannot find a forced mate in this position) |
| engine        | varchar(100)            | Full name of Fairy Stockfish version used for this position's evaluation                                                                                                                                                                                 |
| depth         | smallint                | Depth to which Fairy Stockfish evaluated this position before producing this record's evaluation                                                                                                                                                         |
| depth_limit   | smallint                | Maximum depth setting applied to Fairy Stockfish for this record's evaluation                                                                                                                                                                            |
| time_limit    | smallint                | Maximum time (in seconds) setting applied to Fairy Stockfish for this record's evaluation                                                                                                                                                                |
| created_at    | timestamp with timezone | Time (in UTC) at which this record was created                                                                                                                                                                                                           |
| updated_at    | timestamp with timezone | Time (in UTC) at which this record was most recently updated                                                                                                                                                                                             |
| deleted_at    | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)                                                                                                                                                                                  |

### `games` Table

**A record for each rated Antichess game played on Lichess**

| Column Name           | Data Type               | Description                                                                                                                   |
| --------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| game_id               | bigint                  | Primary key representing a unique rated Antichess game                                                                        |
| lichess_game_id       | varchar(30)             | Unique external Lichess ID for this game                                                                                      |
| event_id              | bigint                  | Foreign key, references events.event_id (can be null if this game did not take place within a Lichess Arena/Swiss Tournament) |
| white_player_id       | bigint                  | Foreign key, references players.player_id, represents the player of the white pieces in this game                             |
| white_player_elo      | smallint                | Elo rating of the white player at the start of this game (rounded to the nearest whole number)                                |
| white_player_elo_diff | smallint                | Number of Elo points the white player gained or lost as a result of this game (rounded to the nearest whole number)           |
| black_player_id       | bigint                  | Foreign key, references players.player_id, represents the player of the black pieces in this game                             |
| black_player_elo      | smallint                | Elo rating of the black player at the start of this game (rounded to the nearest whole number)                                |
| black_player_elo_diff | smallint                | Number of Elo points the black player gained or lost as a result of this game (rounded to the nearest whole number)           |
| avg_player_elo        | smallint                | Average Elo rating between the white and the black player at the start of this game                                           |
| time_control          | varchar(30)             | Lichess-formatted string representing this game's time control (eg. '60+0' is a 1 minute game, no increment)                  |
| time_control_base     | smallint                | Number of seconds each side started with on the clock for this game                                                           |
| time_control_inc      | smallint                | Number of seconds added to each side’s clock per move in this game                                                            |
| termination           | varchar(50)             | Lichess-designated termination for this game                                                                                  |
| result                | varchar(50)             | '1-0' (white won), '0-1' (black won), or '½-½' (draw) or other if terminated abnormally                                       |
| date_utc              | date                    | Date (in UTC) on which this game began                                                                                        |
| time_utc              | timestamp with timezone | Timestamp (in UTC) at which this game began                                                                                   |
| pgn                   | text                    | Full representation of this game in Portable Game Notation (PGN)                                                              |
| created_at            | timestamp with timezone | Time (in UTC) at which this record was created                                                                                |
| updated_at            | timestamp with timezone | Time (in UTC) at which this record was most recently updated                                                                  |
| deleted_at            | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)                                                       |

### `annotations` Table

**A record for each move annotation (eg. '?' for Mistake, '??' for Blunder, etc.)**

| Column Name   | Data Type               | Description                                                             |
| ------------- | ----------------------- | ----------------------------------------------------------------------- |
| annotation_id | bigint                  | Primary key representing an annotation that can be applied to a move    |
| symbol        | varchar(10)             | Symbol for this annotation (eg. '?' for Mistake or '??' for Blunder)    |
| name          | varchar(30)             | Name for this annotation (eg. 'Missed Win', 'Excellent Move')           |
| desc          | varchar(200)            | Detailed description for this annotation                                |
| created_at    | timestamp with timezone | Time (in UTC) at which this record was created                          |
| updated_at    | timestamp with timezone | Time (in UTC) at which this record was most recently updated            |
| deleted_at    | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted) |

### `moves` Table

**A record for each move played in a given rated Antichess game on Lichess**

| Column Name           | Data Type               | Description                                                                                                                                                                                                                         |
| --------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| move_id               | bigint                  | Primary key representing a unique instance of a move played in a rated Antichess game                                                                                                                                               |
| starting_position_id  | bigint                  | Foreign key, references positions.position_id, represents the position at the start of this move                                                                                                                                    |
| resulting_position_id | bigint                  | Foreign key, references positions.position_id, represents the position that resulted from this move                                                                                                                                 |
| player_id             | bigint                  | Foreign key, references players.player_id, represents the player that played this move                                                                                                                                              |
| game_id               | bigint                  | Foreign key, references games.game_id, represents the game in which this move was played                                                                                                                                            |
| annotation_id         | bigint                  | Foreign key, references annotations.annotation_id, represents the annotation for this move (eg. '?? blunder', '!! brilliant', etc.), can be null if this move does not have an appropriate annotation or has not yet been annotated |
| move_number           | smallint                | Represents this move's number for this game; each notated move has two plies (eg. The third move played by white would be move 3 ply 5, and the third move played by black would be move 3 ply 6)                                   |
| ply_number            | smallint                | Represents this move's ply for this game; each notated move has two plies (eg. The third move played by white would be move 3 ply 5, and the third move played by black would be move 3 ply 6)                                      |
| move_notation         | varchar(20)             | Representation of this move in Algebraic notation (eg. '1.Nf3' or '4...h5')                                                                                                                                                         |
| created_at            | timestamp with timezone | Time (in UTC) at which this record was created                                                                                                                                                                                      |
| updated_at            | timestamp with timezone | Time (in UTC) at which this record was most recently updated                                                                                                                                                                        |
| deleted_at            | timestamp with timezone | Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)                                                                                                                                                             |