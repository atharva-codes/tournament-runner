from tournament_runner.model import Model
from tournament_runner.tournament_system import load_tournament_system
from tournament_runner.tournament_storage import load_tournament_storage
from collections import defaultdict


class Player(Model):
    attributes = ['id', 'name', 'rating', 'active', 'fake']


class StandingsPlayer(Model):
    # pos is position of current player in standings
    attributes = ['pos', 'player', 'score']


class Game(Model):
    # pos is position of the game in it's round
    attributes = ['id', 'round', 'pos', 'player_a', 'player_b', 'points_a', 'points_b']


class Tournament(object):
    def __init__(self, name, system, storage):
        self._name    = name
        self._system  = system
        self._storage = storage
        self._players = {}
        self._games   = {}
        self._round   = 0
        
    @property
    def json(self):
      return {
          'name': self._name,
          'players': self._players,
          'games': self._games,
          'round': self._round,
    }


    def enroll(self, **kwargs):
        p = Player(id=len(self._players), fake=False, **kwargs)
        self._players[p.id] = p
        self._storage.update_player(p)

    @property
    def fake_player(self):
        return Player(id=len(self._players), name='bye', rating=0, active=True, fake=True)

    @property
    def fake_player_with_score(self):
        return StandingsPlayer(
            pos    = len(self._players),
            player = self.fake_player,
            score  = 0,
        )

    @property
    def players(self): return self._players.values()

    @property
    def games(self): return self._games.values()

    @property
    def current_round(self): return self._round

    @property
    def current_games(self):
        return [g for g in self.games if g.round == self.current_round]

    @property
    def standings(self):
        '''@return List<StandingsPlayer>'''
        players = {p.id: StandingsPlayer(pos=0, player=p, score=0) for p in self.players if not p.fake}
        for g in self.games:
            if not g.player_a.fake: players[g.player_a.id].score += g.points_a
            if not g.player_b.fake: players[g.player_b.id].score += g.points_b

        result = list(players.values())
        result.sort(key=lambda p: p.score, reverse=True)
        for i, p in enumerate(result): p.pos = i + 1
        return result

    @staticmethod
    def player_pair_key(p1, p2):
        return (min( p1.id, p2.id ), max( p1.id, p2.id ),)

    @property
    def player_pairs_to_games(self):
        cache_key = (len(self.games), len(self.players), self.current_round)
        if not hasattr(self, '_pairs_cache_key') or cache_key != self._pairs_cache_key:
            result = defaultdict(list)
            for g in self.games:
                k = self.player_pair_key(g.player_a, g.player_b)
                result[k].append(g)
            self._pairs_cache_key = cache_key
            self._player_pairs_to_games = result
        return self._player_pairs_to_games

    def get_games_by_players(self, p1, p2):
        return self.player_pairs_to_games[self.player_pair_key(p1, p2)]

    def generate_round(self):
        new_round = self._round + 1
        pairings = self._system.generate_pairings(self)
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
            name    = self._name,
            system  = self._system,
            storage = self._storage,
        )
