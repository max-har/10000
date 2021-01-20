#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:27:03 2021

@author: Max Harder
"""

# %% IMPORT

import random
import sys


def throw(cubes, score=0):
    """throw current number of dice

    param1: number of cubes
    output: current throw"""
    show_score(score)
    this_throw = list((random.randint(1,6) for cube in cubes if cube != 0))
    return this_throw


def put_dice_aside(this_throw, all_aside, score):
    """put dice aside

    param1: current throw
    param2: old score
    output: new score"""
    if 1 not in this_throw and 5 not in this_throw:
        print(f'Sorry, no chance: {this_throw}')
        sys.exit()

    all_aside, now_aside = putting_process(this_throw, all_aside)
    print(f'Is this correct: {all_aside}?')
    leftover_dice = [dice for dice in this_throw if dice not in all_aside]
    calc_score = calculate_score(now_aside)
    # print(score, calc_score)
    score += calc_score
    #print(f'{score} / {calc_score}')
    roll = input('Do you want to roll the dice again? [Y/n] ')
    # continue
    if roll.lower() == 'y':
        print(f'all_aside (FAIL): {all_aside}')
        another_throw = throw(leftover_dice, score)
        #print(f'>> {another_throw}')
        put_dice_aside(another_throw, all_aside, score)
    # end
    else:
        print(f'Aside: {all_aside}')  # correct
        print(f'Leftover: {leftover_dice}')
        #show_score(score)
        del all_aside
        sys.exit()
    return score
# TO DO: PUTTING ASIDE MUST BE REMEMBERED AND VISUALISED


def putting_process(this_throw, all_aside=None):  # BUGGY!
    """validate putting process

    param1: current throw
    param2: all dice aside (default: None)
    output: all dice aside, current dice aside"""

    print(f'{this_throw} | {all_aside}')  # DISPLAY DICE

    now_aside = input('Which dice do you want to put aside? ')
    # prevent ValueError
    if now_aside.isdigit():
        #all_aside = [int(dice) for dice in all_aside]
        now_aside = [int(dice) for dice in now_aside]
    else:
        raise ValueError('Not all elements are integers.')

    if not all_aside:
        all_aside = now_aside+[]  # debug (missing double digit)
        print(f'test: {all_aside}')
    else:
        all_aside += now_aside
        print(f'test: {all_aside}')

    if not validator(this_throw, now_aside, special=True):
        print('You can not put this set of dice aside.')
        all_aside = []
        putting_process(this_throw, all_aside)

    print(f'This is aside: {all_aside}')
    return all_aside, now_aside
# to do: two triples is not a failure!
# bug: can choose 1 3 3 3 from [1, 4]
# bug: street and three_pairs fails ("[1, 1, 1, 1, 1, 1]")


def validator(this_throw, now_aside=False, special=False):
    """check whether decision is valid

    param1:
    param2:
    output: """

    street = list(range(1,7))
    three_pairs = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 2]) == 6
    two_triples = sum([1 for each_dice in this_throw if
                       this_throw.count(each_dice) == 3]) == 6  # new

    sorted(this_throw)
    if (this_throw is street or
        this_throw is three_pairs or
        this_throw is two_triples):
        return True
    if special:
        for cube in now_aside:
            if cube in (1, 5) or now_aside.count(cube) >= 3:
                return True
    return False

def calculate_score(now_aside):
    """calculate score"""

    calc_score = 0
    special_score = 1500

    if validator(now_aside):
        calc_score += special_score
        print(f'STREET OR THREE PAIRS: {calc_score}')

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


def show_score(score):
    """show score"""
    current_score = f'| {score:,} / 10,000 |'
    print('+'+(len(current_score)-2)*'-'+'+')
    print(current_score)
    print('+'+(len(current_score)-2)*'-'+'+')
    #return score


def play():
    """play one round"""
    score = 0
    cubes_aside = []
    cubes = [1, 1, 1, 1, 1, 1]
    while score < 10000:
        this_throw = throw(cubes, score)
        calc_score = put_dice_aside(this_throw, cubes_aside, score)
        print(calc_score)
        score += calc_score
        print(score)
        break

# %% EXECUTE

if __name__ == "__main__":
    play()

# %%

