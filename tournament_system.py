from helpers import Model, chunker
from random import shuffle


class StandingsPlayer(Model):
    # pos is position of current player in standings
    attributes = ['pos', 'player', 'score']


class RoundPlayerPairing(Model):
    # pos is the game's board number in current round
    attributes = ['pos', 'player_a', 'player_b']


class TournamentSystem(object):
    def generate_pairings(self, tournament, round):
        '''@returns List<RoundPlayerPairing>'''
        raise NotImplementedError('Oops!')

    def get_standings(self, tournament, round):
        '''@return List<StandingsPlayer>'''
        players = { p_id: StandingsPlayer(pos=0, player=tournament.p(p_id), score=0) for p_id in tournament.players }
        for g_id in tournament.games:
            g = tournament.games[g_id]
            players[g.player_a.id].score += g.points_a
            players[g.player_b.id].score += g.points_b
        result = [players[p_id] for p_id in players]
        result.sort(key=lambda p: p.score, reverse=True)
        for i, p in enumerate(result):
            p.pos = i + 1
        return result

class SwissSystem(TournamentSystem):
    def __init__(self, rounds):
        self._rounds = rounds

    def generate_pairings(self, tournament, round):
        player_ids = [p_id for p_id in tournament.players]
        shuffle(player_ids)
        result = []
        pos = 0
        for chunk in chunker(player_ids, 2):
            pos += 1
            if len(chunk) < 2:
                break
            result.append(RoundPlayerPairing(
                pos = pos,
                player_a = tournament.p(chunk[0]),
                player_b = tournament.p(chunk[1]),
            ))
        return result

def load_tournament_system(system_name, **kwargs):
    if system_name == 'swiss':
        return SwissSystem(**kwargs)
    raise NotImplementedError('System {} not implemented!'.format(name))
