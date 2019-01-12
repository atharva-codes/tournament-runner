#!/usr/bin/env python3
from tournament import TournamentFactory
import random
import string

def _random_name(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def display_standings(standings):
    for row in standings:
        print('{:2}. {} ({})\t{}'.format(row.pos, row.player.name, row.player.rating, row.score))
    print()

def display_pairings(pairings):
    for row in pairings:
        print('{:2}. {}\t{} : {}\t{}'.format(
            row.pos,
            row.player_a.name,
            row.points_a,
            row.points_b,
            row.player_b.name,
        ))
    print()

if __name__ == '__main__':
    t = TournamentFactory() \
        .name(_random_name(15)) \
        .system('dummy', rounds=9) \
        .storage('dummy') \
        .load()

    for i in range(random.randrange(15) + 1):
        t.enroll(
            name   = 'Player ' + (chr(ord('A') + i)),
            rating = 1800 + random.randrange(400),
            active = True,
        )

    for round in range(9):
        t.generate_round()

        print('== Standings before round {} =='.format(t.current_round))
        display_standings(t.get_standings())

        for g in t.current_games:
            if g.player_a.rating > g.player_b.rating:
                points_a, points_b = 1, 0
            elif g.player_a.rating < g.player_b.rating:
                points_a, points_b = 0, 1
            else:
                points_a, points_b = 0.5, 0.5
            t.set_result(g, points_a, points_b)

        print('== Pairings after round {} =='.format(t.current_round))
        display_pairings(t.current_games)

    print('== Final standings ==')
    display_standings(t.get_standings())
