from helpers import Model
from tournament_system import load_tournament_system
from tournament_storage import load_tournament_storage


class Player(Model):
    attributes = ['id', 'name', 'rating', 'active']


class Game(Model):
    attributes = ['id', 'round', 'pos', 'player_a', 'player_b', 'points_a', 'points_b']


class Tournament(object):
    def __init__(self, name, system, storage):
        self._name    = name
        self._system  = system
        self._storage = storage
        self._players = {}
        self._games   = {}
        self._round   = 0

    def new_player(self, **kwargs):
        p = Player(id=len(self._players), **kwargs)
        self._players[p.id] = p
        self._storage.update_player(p)

    def p(self, p_id): return self._players[p_id]
    def g(self, g_id): return self._games[g_id]

    @property
    def players(self): return self._players

    @property
    def games(self): return self._games

    @property
    def current_round(self): return self._round

    @property
    def current_games(self):
        return [self._games[g_id] for g_id in self._games if self._games[g_id].round == self.current_round]

    def get_standings(self, round=None):
        return self._system.get_standings(self, round or self.current_round)

    # we want flexibility to potentially regenerate a bad round
    def generate_round(self, round=None):
        new_round = round or (self._round + 1)
        pairings = self._system.generate_pairings(self, new_round)
        for p in pairings:
            g = Game(
                id  = len(self._games),
                pos = p.pos,
                player_a = p.player_a,
                player_b = p.player_b,
                points_a = 0,
                points_b = 0,
                round = new_round,
            )
            self._games[g.id] = g
            self._storage.update_game(g)
        self._round = new_round

    def set_result(self, game, points_a, points_b):
        g = self._games[game.id]
        g.points_a, g.points_b = points_a, points_b
        self._storage.update_game(g)


class TournamentFactory(object):
    _name    = None
    _system  = None
    _storage = None

    def name(self, value):
        self._name = value
        return self

    def system(self, system_name, *args, **kwargs):
        self._system = load_tournament_system(system_name, **kwargs)
        return self

    def storage(self, storage_type):
        self._storage = load_tournament_storage(storage_type)
        return self

    def load(self):
        if any([
            self._name    is None,
            self._system  is None,
            self._storage is None,
        ]):
            raise ValueError("Error: need all arguments!")
        return Tournament(
            name    = self.name,
            system  = self._system,
            storage = self._storage,
        )
