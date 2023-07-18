#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:27:03 2021.

@author: Max Harder
"""

# %% IMPORT

import random
import sys

from copy import deepcopy

WELCOME = r''' _               _   _                                     _
| |_ ___ _ __   | |_| |__   ___  _   _ ___  __ _ _ __   __| |
| __/ _ \ '_ \  | __| '_ \ / _ \| | | / __|/ _` | '_ \ / _` |
| ||  __/ | | | | |_| | | | (_) | |_| \__ \ (_| | | | | (_| |
 \__\___|_| |_|  \__|_| |_|\___/ \__,_|___/\__,_|_| |_|\__,_|

https://github.com/max-har/10000                   2023-07-18'''

THRESHOLD = 350


def play():
    """Play one game."""
    score = 0
    print(WELCOME)
    while score < 10000:
        tmp_points = 0
        cubes_aside = []
        cubes = range(1, 7)  # six cubes

        print('\nNEW ROUND!')

        draw_box(score)
        tmp_points = put_dice_aside(cubes, cubes_aside, tmp_points)
        score += tmp_points
        draw_box(score)

    print('10,000!')


def throw(cubes):
    """Throw current number of dice.

    param1: number of cubes
    output: current throw
    """
    this_throw = list((random.randint(1, 6) for cube in cubes if cube != 0))
    # this_throw = [1,1,1,1,5,5]  # debugging
    draw_dice(this_throw)
    return this_throw


def draw_dice(this_throw):
    """Draw current number of dice."""
    cube_top = '┌───┐'
    cube_mid = '│ {} │'
    cube_bot = '└───┘'
    # ┌ ┐ ─ ┬ ┴ └ ┘
    this_cube_top, this_cube_mid, this_cube_bot = '', '', ''
    for dice in this_throw:
        this_cube_top += cube_top
        this_cube_mid += cube_mid.format(dice)
        this_cube_bot += cube_bot
    print(this_cube_top + '\n' + this_cube_mid + '\n' + this_cube_bot)


def draw_box(min_val, max_val=THRESHOLD, score=True):
    """Draw a box showing the current score or points."""
    if score:
        current_score = f'│ {min_val:,} / 10,000 │'
        print('\n┌' + (len(current_score) - 2) * '─' + '┐')
        print(current_score)
        print('└' + (len(current_score) - 2) * '─' + '┘\n')
    else:
        current_score = f'│ {min_val:,} / {max_val} │'
        print('\n┌' + (len(current_score) - 2) * '─' + '┐')
        print(current_score)
        print('└' + (len(current_score) - 2) * '─' + '┘\n')


def put_dice_aside(cubes, all_aside, tmp_points=0):
    """Put dice aside.

    param1: current throw
    param2: old score
    output: new score
    """
    this_throw = throw(cubes)

    if validate_throw(this_throw) == 0:
        return 0

    # decision making
    all_aside, now_aside = decision_making(this_throw, all_aside)
    all_aside_copy = deepcopy(all_aside)
    leftover_dice = [dice for dice in this_throw if dice not in all_aside_copy
                     or all_aside_copy.remove(dice)]
    if tmp_points:
        tmp_points += calculate_points(now_aside)
    else:
        tmp_points = calculate_points(now_aside)
    draw_box(tmp_points, score=False)
    if len(all_aside) < 6:
        cont_run = input('Do you want to continue this run? [Y/n] ')
    else:
        # all dice aside
        cont_run = input('No dice left! Do you want to continue this run? [Y/n] ')
        if not cont_run.lower() == 'y':
            return tmp_points
        return put_dice_aside(cubes, [], tmp_points)
    # continue
    if cont_run.lower() == 'y':
        return put_dice_aside(leftover_dice, all_aside, tmp_points)
    # end
    draw_box(tmp_points, score=False)
    if tmp_points < THRESHOLD:
        print(f'Your points ({tmp_points}) are below the threshold ({THRESHOLD}).')
        return 0
    return tmp_points


def validate_throw(this_throw):  # BUG?
    """Validate throw."""
    if not validator(this_throw, init=True):
        print('No chance!')
        roll_again = input('Do you want to roll the dice again? [Y/n] ')
        if not roll_again.lower() == 'y':
            sys.exit()
        else:
            return 0
    return True


def decision_making(this_throw, all_aside=None):  # BUG?
    """Manage decision making process.

    param1: current throw
    param2: all dice aside (default: None)
    output: all dice aside, current dice aside
    """
    print(f'\n{all_aside}\n')  # DISPLAY DICE ASIDE
    while True:
        now_aside = input('Which dice do you want to put aside? ')
        if now_aside.isdigit():
            now_aside = [int(dice) for dice in now_aside]
            break
        elif ' ' in now_aside and ''.join(now_aside.split()).isdigit():
            now_aside = [int(digit) for digit in now_aside.split()]
            break
        else:
            print('Please enter integers only.')

    if not all_aside:
        all_aside = list(now_aside)
    else:
        all_aside += list(now_aside)

    if not validator(now_aside):
        print('You cannot put this set of dice aside.')
        all_aside = []
        decision_making(this_throw, all_aside)

    return all_aside, now_aside


def validator(this_throw, init=False, special=False):
    """Check whether decision is valid.

    param1:
    param2:
    param3: special (street, doubles, pairs, triples)
    output: boolean value
    """

    valid_dice = [cube for cube in this_throw if cube in (1, 5) or
                  this_throw.count(cube) >= 3]
    invalid_dice = [cube for cube in this_throw if cube not in (1, 5) and
                    this_throw.count(cube) < 3]

    sorted(this_throw)
    if init:
        if valid_dice or is_special(this_throw):
            return True
        return False
    if special:
        if is_special(this_throw):
            return True
        return False
    if (valid_dice and not invalid_dice) or is_special(this_throw):
        return True
    return False


def is_special(this_throw):
    """Check if set of dice is special (street, three pairs, two triples)."""
    street = list(range(1, 7))
    three_pairs = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 2]) == 6
    two_triples = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 3]) == 6

    if this_throw == street or three_pairs or two_triples:
        return True
    return False


def calculate_points(now_aside):
    """Calculate score of decision."""
    tmp_points = 0
    special_points = 1500

    # special throw (street etc.)
    if validator(now_aside, special=True):
        tmp_points += special_points
        # print(f'{tmp_points}')
        return tmp_points

    # doubles (plus ones and fives)
    for each_dice in now_aside:
        if now_aside.count(each_dice) >= 3:
            while now_aside.count(each_dice) > 3:
                tmp_points += 1000
                now_aside.remove(each_dice)
            if each_dice != 1:
                tmp_points += each_dice * 100
            else:
                tmp_points += 1000
            now_aside.remove(each_dice)
            # filter remaining ones and fives
            one_five_aside = [dice for dice in now_aside if dice != each_dice]
            # print(f'Ones and fives aside: {one_five_aside}')  # OK
            # is there still a bug when an invalid move is followed by a double?
            remaining_points = one_five_score(one_five_aside)
            tmp_points += remaining_points
            return tmp_points

    # only ones and fives
    standard_points = one_five_score(now_aside)
    tmp_points += standard_points
    return tmp_points


def one_five_score(preproc_aside):
    """Calculate score from ones and fives.

    param1: all dice aside
    param2: current score (default: empty list)
    output: score
    """
    remaining_points = sum([50 if dice == 5 else 100 for dice in preproc_aside
                            if dice in (1, 5)])
    return remaining_points


if __name__ == "__main__":
    play()

# %% PLAYGROUND
