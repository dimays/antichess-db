from django.db import models


class Player(models.Model):
    player_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a Lichess user who has played at least one rated Antichess game"
        )
    lichess_username = models.CharField(
        max_length=30,
        unique=True,
        db_comment="Unique username for this Lichess player (always represented in lowercase)"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "players"
        db_table_comment = "A record for each player on Lichess who has played at least one rated Antichess game"

    def __str__(self):
        str_rep = f"({self.player_id}) {self.lichess_username}"
        return str_rep


class Event(models.Model):
    event_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a Lichess event"
        )
    lichess_event_id = models.CharField(
        max_length=30,
        unique=True,
        db_comment="Unique, external Lichess ID for this Lichess event, prefixed with 'swiss-' if a Swiss tournament, prefixed with 'arena-' if an Arena tournament"
        )
    event_name = models.CharField(
        max_length=30,
        db_comment="Name for this Lichess event"
        )
    start_date_utc = models.DateField(
        db_comment="Date (in UTC) on which this event began"
        )
    start_time_utc = models.DateTimeField(
        db_comment="Timestamp (in UTC) at which this event began"
        )
    duration_minutes = models.SmallIntegerField(
        db_comment="Number of minutes this event lasted"
        )
    first_place_player = models.ForeignKey(
        Player,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='first_place_players',
        db_comment="Foreign key, references players.player_id, represents the player that won this event"
        )
    second_place_player = models.ForeignKey(
        Player,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='second_place_players',
        db_comment="Foreign key, references players.player_id, represents the player that got second place at this event")
    third_place_player = models.ForeignKey(
        Player,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        related_name='third_place_players',
        db_comment="Foreign key, references players.player_id, represents the player that got third place at this event")
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "events"
        db_table_comment = "A record for each Lichess event (Arena or Swiss Tournament) during which at least one rated Antichess game was played"

    def __str__(self):
        str_rep = f"({self.event_id}) {self.event_name}"
        return str_rep
  

class Position(models.Model):
    position_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique board position"
        )
    fen = models.CharField(
        max_length=100,
        db_comment="Representation of this position in abbreviated Forsyth-Edwards Notation (FEN), does not include some fields which are not necessary for the purposes of evaluating the position, such as move number"
        )
    eval = models.CharField(
        max_length=20,
        db_comment="Formatted string representing a centipawn value (eg. '-1.3') or a forced mate (eg. '#7')"
        )
    cp = models.DecimalField(
        max_digits=9,
        decimal_places=1,
        null=True,
        default=None,
        db_comment="Fairy Stockfish’s centipawn evaluation for this position, with one decimal place (can be NULL if evaluation is a forced mate instead)"
        )
    mate = models.SmallIntegerField(
        null=True,
        default=None,
        db_comment="Fairy Stockfish’s evaluation of the minimum number of moves until mate for this position, expressed as a positive if a mate for white, and as a negative if a mate for black (can be NULL if Fairy Stockfish cannot find a forced mate in this position)"
        )
    engine = models.CharField(
        max_length=100,
        db_comment="Full name of Fairy Stockfish version used for this position's evaluation"
        )
    depth = models.SmallIntegerField(
        db_comment="Depth to which Fairy Stockfish evaluated this position before producing this record's evaluation"
        )
    depth_limit = models.SmallIntegerField(
        db_comment="Maximum depth setting applied to Fairy Stockfish for this record's evaluation"
        )
    time_limit = models.SmallIntegerField(
        db_comment="Maximum time (in seconds) setting applied to Fairy Stockfish for this record's evaluation"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "positions"
        db_table_comment = "A record for each unique position that has been achieved in at least one rated Antichess game on Lichess"

    def __str__(self):
        str_rep = f"({self.position_id}) {self.fen}"
        return str_rep


class Game(models.Model):
    game_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique rated Antichess game"
        )
    lichess_game_id = models.CharField(
        max_length=30,
        unique=True,
        db_comment="Unique external Lichess ID for this game"
        )
    event = models.ForeignKey(
        Event,
        null=True,
        default=None,
        on_delete=models.PROTECT,
        db_comment="Foreign key, references events.event_id (can be null if this game did not take place within a Lichess Arena/Swiss Tournament)"
        )
    white_player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='white_players',
        db_comment="Foreign key, references players.player_id, represents the player of the white pieces in this game"
        )
    white_player_elo = models.SmallIntegerField(
        db_comment="Elo rating of the white player at the start of this game (rounded to the nearest whole number)"
        )
    white_player_elo_diff = models.SmallIntegerField(
        db_comment="Number of Elo points the white player gained or lost as a result of this game (rounded to the nearest whole number)"
        )
    black_player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='black_players',
        db_comment="Foreign key, references players.player_id, represents the player of the black pieces in this game"
        )
    black_player_elo = models.SmallIntegerField(
        db_comment="Elo rating of the black player at the start of this game (rounded to the nearest whole number)"
        )
    black_player_elo_diff = models.SmallIntegerField(
        db_comment="Number of Elo points the black player gained or lost as a result of this game (rounded to the nearest whole number)"
        )
    avg_player_elo = models.SmallIntegerField(
        db_comment="Average Elo rating between the white and the black player at the start of this game"
        )
    time_control = models.CharField(
        max_length=30,
        db_comment="Lichess-formatted string representing this game's time control (eg. '60+0' is a 1 minute game, no increment)"
        )
    time_control_base = models.SmallIntegerField(
        db_comment="Number of seconds each side started with on the clock for this game"
        )
    time_control_inc = models.SmallIntegerField(
        db_comment="Number of seconds added to each side’s clock per move in this game"
        )
    termination = models.CharField(
        max_length=50,
        db_comment="Lichess-designated termination for this game"
        )
    result = models.CharField(
        max_length=50,
        db_comment="'1-0' (white won), '0-1' (black won), or '½-½' (draw) or other if terminated abnormally"
        )
    date_utc = models.DateField(
        db_comment="Date (in UTC) on which this game began"
        )
    time_utc = models.DateTimeField(
        db_comment="Timestamp (in UTC) at which this game began"
        )
    pgn = models.TextField(
        db_comment="Full representation of this game in Portable Game Notation (PGN)"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "games"
        db_table_comment = "A record for each rated Antichess game played on Lichess"

    def __str__(self):
        str_rep = f"({self.game_id}) {self.white_player_elo} v. {self.black_player_elo}"
        return str_rep


class Annotation(models.Model):
    annotation_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing an annotation that can be applied to a move"
        )
    symbol = models.CharField(
        max_length=10,
        db_comment="Symbol for this annotation (eg. '?' for Mistake or '??' for Blunder)"
        )
    name = models.CharField(
        max_length=30,
        db_comment="Name for this annotation (eg. 'Missed Win', 'Excellent Move')"
        )
    desc = models.CharField(
        max_length=200,
        db_comment="Detailed description for this annotation"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )

    class Meta:
        db_table = "annotations"
        db_table_comment = "A record for each move annotation (eg. '?' for Mistake, '??' for Blunder, etc.)"

    def __str__(self):
        str_rep = f"({self.annotation_id}) {self.symbol}"
        return str_rep


class Move(models.Model):
    move_id = models.BigAutoField(
        primary_key=True,
        db_comment="Primary key representing a unique instance of a move played in a rated Antichess game"
        )
    starting_position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name='starting_positions',
        db_comment="Foreign key, references positions.position_id, represents the position at the start of this move"
        )
    resulting_position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name='resulting_positions',
        db_comment="Foreign key, references positions.position_id, represents the position that resulted from this move"
        )
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        db_comment="Foreign key, references players.player_id, represents the player that played this move")
    game = models.ForeignKey(
        Game,
        on_delete=models.PROTECT,
        db_comment="Foreign key, references games.game_id, represents the game in which this move was played")
    annotation = models.ForeignKey(
        Annotation,
        on_delete=models.PROTECT,
        null=True,
        db_comment="Foreign key, references annotations.annotation_id, represents the annotation for this move (eg. '?? blunder', '!! brilliant', etc.), can be null if this move does not have an appropriate annotation or has not yet been annotated"
        )
    move_number = models.SmallIntegerField(
        db_comment="Represents this move's number for this game; each notated move has two plies (eg. The third move played by white would be move 3 ply 5, and the third move played by black would be move 3 ply 6)"
        )
    ply_number = models.SmallIntegerField(
        db_comment="Represents this move's ply for this game; each notated move has two plies (eg. The third move played by white would be move 3 ply 5, and the third move played by black would be move 3 ply 6)"
        )
    move_notation = models.CharField(
        max_length=20,
        db_comment="Representation of this move in Algebraic notation (eg. '1.Nf3' or '4...h5')"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Time (in UTC) at which this record was created"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_comment="Time (in UTC) at which this record was most recently updated"
        )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        db_comment="Time (in UTC) at which this record was 'soft-deleted' (flagged deleted)"
        )
    
    class Meta:
        db_table = "moves"
        db_table_comment = "A record for each move played in a given rated Antichess game on Lichess"

    def __str__(self):
        str_rep = f"({self.move_id}) {self.lichess_username}"
        return str_rep
