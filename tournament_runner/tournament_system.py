from tournament_runner.model import Model
from random import shuffle, choice

class RoundPlayerPairing(Model):
    # pos is the game's board number in current round
    attributes = ['pos', 'player_a', 'player_b']


def _log(*args):
    # print(*args)
    pass

# see https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
def _chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class TournamentSystem(object):
    def generate_pairings(self, tournament):
        '''@returns List<RoundPlayerPairing>'''
        raise NotImplementedError('Oops!')


class DummySystem(TournamentSystem):
    '''pair up 2 random opponents every time'''
    def __init__(self, rounds):
        # just an example of passing params, not really used
        self._rounds = rounds

    def generate_pairings(self, tournament):
        players = [p for p in tournament.players if p.active]
        shuffle(players)
        result = []
        pos = 0
        for chunk in _chunker(players, 2):
            pos += 1
            if len(chunk) < 2:
                break
            result.append(RoundPlayerPairing(
                pos = pos,
                player_a = chunk[0],
                player_b = chunk[1],
            ))
        return result



class SwissSystemError(Exception):
    pass


class SwissSystem(TournamentSystem):
    '''
    swiss with bruteforce mpv implementation
    '''
    def _check_can_play(self, tournament, p1, p2):
        return len(tournament.get_games_by_players(p1.player, p2.player)) == 0

    def _find_possible_opponents(self, tournament, p, players, impossible_opponents):
        possible_opponents = set()
        possible_score     = 0
        for opp in players:
            if opp in impossible_opponents or not self._check_can_play(tournament, p, opp):
                _log(' x', opp)
                continue
            if len(possible_opponents) == 0 or opp.score > possible_score:
                possible_opponents = set([opp])
                possible_score = opp.score
            elif opp.score == possible_score:
                possible_opponents.add(opp)
        return possible_opponents

    def _pop_top_player(self, players):
        max_score = max(players, key=lambda p: p.score).score
        top_player = choice([p for p in players if p.score == max_score])
        players.remove(top_player)
        return top_player

    def _run(self, tournament, players, pairs):
        if len(players) == 0:
            return True

        p = self._pop_top_player(players)

        impossible_opponents = set()
        while True:
            _log('Pivot  ::', p)
            possible_opponents = self._find_possible_opponents(tournament, p, players, impossible_opponents)
            if len(possible_opponents) == 0:
                _log(' - no possible opponents! Putting Pivot back.')
                players.add(p)
                return False

            for opp in possible_opponents:
                _log(' -', opp)
            opp = choice(list(possible_opponents))
            players.remove(opp)
            _log('Chosen ::', opp)

            if self._run(tournament, players, pairs):
                pairs.append((p, opp))
                return True
            else:
                impossible_opponents.add(opp)
                players.add(opp)

    def generate_pairings(self, tournament):
        players = set([p for p in tournament.standings if p.player.active])

        # for p in players: _log(' v', p)

        if len(players) % 2 == 1:
            players.add(tournament.fake_player_with_score)

        pairs = []
        if self._run(tournament, set(players), pairs):
            pairs.reverse()
            return [RoundPlayerPairing(
                pos = i + 1,
                player_a = pp[0].player,
                player_b = pp[1].player,
            ) for (i, pp) in enumerate(pairs)]

        raise SwissSystemError("Impossible happened, we cannot generate pairings!")


def load_tournament_system(system_name, **kwargs):
    if system_name == 'dummy':
        return DummySystem(**kwargs)
    elif system_name == 'swiss':
        return SwissSystem()
    raise NotImplementedError('System {} not implemented!'.format(name))
