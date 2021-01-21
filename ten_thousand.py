#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:27:03 2021

@author: Max Harder
"""

# %% IMPORT

import random
import sys


WELCOME = r''' _               _   _                                     _
| |_ ___ _ __   | |_| |__   ___  _   _ ___  __ _ _ __   __| |
| __/ _ \ '_ \  | __| '_ \ / _ \| | | / __|/ _` | '_ \ / _` |
| ||  __/ | | | | |_| | | | (_) | |_| \__ \ (_| | | | | (_| |
 \__\___|_| |_|  \__|_| |_|\___/ \__,_|___/\__,_|_| |_|\__,_|

https://github.com/max-har/10000     ¯\_(ツ)_/¯    2021-01-21'''


def play():
    """play one round"""
    score = 0
    cubes_aside = []
    cubes = range(1,7)  # six cubes
    print(WELCOME)
    while score < 10000:
        this_throw = throw(cubes, score)
        calc_score = put_dice_aside(this_throw, cubes_aside, score)
        print(calc_score)
        score += calc_score
        print(score)
        break


def throw(cubes, score=0):
    """throw current number of dice

    param1: number of cubes
    output: current throw"""
    show_score(score)
    this_throw = list((random.randint(1,6) for cube in cubes if cube != 0))
    return this_throw


def show_score(score):
    """show score"""
    current_score = f'| {score:,} | 10,000 |'
    print('\n+'+(len(current_score)-2)*'-'+'+')
    print(current_score)
    print('+'+(len(current_score)-2)*'-'+'+\n')
    #return score


def put_dice_aside(this_throw, all_aside, score):
    """put dice aside

    param1: current throw
    param2: old score
    output: new score"""
    if not validator(this_throw, init=True):  # remove only_special
        print(f'Sorry, no chance: {this_throw}')
        roll = input('Do you want to roll the dice again? [Y/n] ')
        if not roll.lower() == 'y':
            #show_score(score)
            sys.exit()

    all_aside, now_aside = putting_process(this_throw, all_aside)
    leftover_dice = [dice for dice in this_throw if dice not in all_aside
                     or all_aside.remove(dice)]  # Bug?
    calc_score = calculate_score(now_aside)
    score += calc_score
    roll = input('Do you want to roll the dice again? [Y/n] ')
    # continue
# BUG
    if roll.lower() == 'y':
        print(f'all_aside (FAIL): {all_aside}')
        another_throw = throw(leftover_dice, score)
        put_dice_aside(another_throw, all_aside, score)
    # end
    else:
        show_score(score)
        #print(f'{leftover_dice}, {all_aside}')  # correct
        del all_aside
        sys.exit()
    return score


def putting_process(this_throw, all_aside=None):  # BUGGY!
    """validate putting process

    param1: current throw
    param2: all dice aside (default: None)
    output: all dice aside, current dice aside"""

    print(f'{this_throw} | {all_aside}')  # DISPLAY DICE

# BUGS

# Which dice do you want to put aside? 24534
# You put aside: [2, 4, 5, 3, 4]
# 50 / 350.
# OR
# Which dice do you want to put aside? 1112
# You put aside: [1, 1, 1, 2]
# DOUBLES: 1000
# one_five_aside: [2]
# 1000 / 350.
# >> you can make invalid moves when combined with a valid decision

# Sorry, no chance: [4, 3, 3, 2, 4, 3]
# >> you can not use streets or doubles

    now_aside = input('Which dice do you want to put aside? ')
    # prevent ValueError
    if now_aside.isdigit():
        #all_aside = [int(dice) for dice in all_aside]
        now_aside = [int(dice) for dice in now_aside]
    elif ' ' in now_aside and ''.join(now_aside.split()).isdigit():
        now_aside = [int(digit) for digit in now_aside.split()]
    else:
        raise ValueError('Not all elements are integers.')

    if not all_aside:
        all_aside = now_aside+[]  # debugging (missing double digit)
        #print(f'test: {all_aside}')
    else:
        all_aside += now_aside
        #print(f'test: {all_aside}')

    if not validator(now_aside):  # BUG!
        print('You cannot put this set of dice aside.')
        all_aside = []
        putting_process(this_throw, all_aside)

    print(f'You put aside: {all_aside}')
    return all_aside, now_aside
# to do: two triples is not a failure!
# bug: can choose 1 3 3 3 from [1, 4]
# bug: street and three_pairs fails ("[1, 1, 1, 1, 1, 1]")


def validator(this_throw, init=False):
    """check whether decision is valid

    param1:
    param2:
    param3: special (street, doubles, pairs, triples)
    output: boolean value"""

    street = list(range(1,7))
    three_pairs = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 2]) == 6
    two_triples = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 3]) == 6  # new

    valid_dice = [cube for cube in this_throw if cube in (1, 5) or
                  this_throw.count(cube) >= 3]
    invalid_dice = [cube for cube in this_throw if cube not in (1, 5) and
                    this_throw.count(cube) < 3]

    sorted(this_throw)
    if init:
        if (valid_dice or
            this_throw is street or
            this_throw is three_pairs or
            this_throw is two_triples):
            return True
        return False
    if ((valid_dice and not invalid_dice) or
        this_throw is street or
        this_throw is three_pairs or
        this_throw is two_triples):
        return True
    return False

def calculate_score(now_aside):
    """calculate score"""

    calc_score = 0
    special_score = 1500

    if validator(now_aside):
        calc_score += special_score
        print(f'SPECIAL: {calc_score}')

    for each_dice in now_aside:
        # doubles
        if now_aside.count(each_dice) >= 3:
            while now_aside.count(each_dice) > 3:
                calc_score += 1000
            if each_dice != 1:
                calc_score += each_dice*100
            else:
                calc_score += 1000
            now_aside.remove(each_dice)
            print(f'DOUBLES: {calc_score}')  # OK

            # filter remaining ones and fives
            one_five_aside = [dice for dice in now_aside if dice != each_dice]
            print(f'one_five_aside: {one_five_aside}')  # OK

            # one five
            calc_score = one_five_score(one_five_aside, calc_score)
            #calc_score += one_five
            return calc_score

    # one–five score
    simple_score = one_five_score(now_aside, calc_score)
    return simple_score
# bug: 1 3 3 3 = 700 (actually 350); 1 1 1 1 = 4000 (actually 2000)
# bug: street 1650 instead of 1500

# BUG
# Which dice do you want to put aside? 331166
# You put aside: [3, 3, 1, 1, 6, 6]
# 200 / 350.
# >> two triples


def one_five_score(preproc_aside, calc_score=0):
    """calculate score from ones and fives

    param1: all dice aside
    param2: current score (default: empty list)
    output: score"""
    threshold = 350
    simple_score = sum([50 if dice == 5 else 100 for dice in preproc_aside
                        if dice in (1, 5)])
    calc_score += simple_score
    print(f'{calc_score} / {threshold}.')
    return calc_score



# BUG
# one_five_aside: [3, 3, 3]

# %% EXECUTE


if __name__ == "__main__":
    play()

# %%

random_throw = [1,2,3,4,5,6]  # True
valid_put = [1, 5]  # True
valid_put_single = [1]  # True
invalid_put = [1, 2]  # False
invalid_put_single = [2]  # False

print(validator(random_throw, init=True))
print(validator(valid_put, init=False))
print(validator(valid_put_single, init=False))
print(validator(invalid_put, init=False))
print(validator(invalid_put_single, init=False))

#print([cube for cube in this_throw if cube not in (1, 5) and this_throw.count(cube) < 3])
