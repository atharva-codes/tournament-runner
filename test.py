#!/usr/bin/env python3
from tournament import TournamentFactory
from tournament_system import SwissSystemError
import random
import string

def _random_name(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def display_standings(standings):
    for row in standings:
        print('{:2}. {} ({})\t{}'.format(row.pos, row.player.name, row.player.rating, row.score))

def display_pairings(pairings):
    for row in pairings:
        print('{:2}. {} ({})\t{} : {} \t{} ({})'.format(
            row.pos,
            row.player_a.name,
            row.player_a.rating,
            row.points_a,
            row.points_b,
            row.player_b.name,
            row.player_b.rating,
        ))

def _outcome(p1, p2):
    if p1.rating > p2.rating:
        return (1, 0)
    elif p1.rating < p2.rating:
        return (0, 1)
    return (0.5, 0.5)

def _run(total_players, total_rounds, verbose=False):
    t = TournamentFactory().name(_random_name(5)).system('swiss').storage('dummy').load()

    for i in range(total_players):
        t.enroll(
            name   = 'Player ' + (chr(ord('A') + i)),
            rating = 1800 + random.randrange(400),
            active = True,
        )

    for round in range(total_rounds):
        if verbose:
            print()
            print('== Generating round {} =='.format(round))
        t.generate_round()

        if verbose:
            print()
            print('== Standings before round {} =='.format(t.current_round))
            display_standings(t.standings)

        for g in t.current_games:
            points_a, points_b = _outcome(g.player_a, g.player_b)
            t.set_result(g, points_a, points_b)

        if verbose:
            print()
            print('== Pairings after round {} =='.format(t.current_round))
            display_pairings(t.current_games)

    if verbose:
        print()
        print('== Final standings ==')
        display_standings(t.standings)


if __name__ == '__main__':
    total_errors = 0
    for i in range(1000):
        try:
            total_players = random.randint(4, 20)
            max_rounds    = total_players - 3
            total_rounds  = max_rounds
            _run(total_players, total_rounds)
            if i % 100 == 1:
                print('ok {}'.format(i))
        except SwissSystemError:
            total_errors += 1
            print('fail {}: players {}, rounds {}'.format(i, total_players, total_rounds))
    print('Errors: {} / 1000'.format(total_errors))
