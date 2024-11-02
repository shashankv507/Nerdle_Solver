# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 01:35:00 2024

@author: shash
"""

from SolveNerdle import Game, Equation
from tqdm import tqdm
from multiprocessing import Pool

def test_game(ANSWER):
    try:
        count = -1
        length = len(ANSWER)
        game = Game(ANSWER)
        eq = Equation(length)
        headstart = 0
        # Uncomment if you want to start with Pre defined equation
        sub0 = eq.equation_preset()
        feedback = game.submit(sub0)
        eq.update_feedback(feedback)
        headstart = 1
        for i in range(headstart, 50):
            sub = eq.execute()
            if sub==ANSWER:
                # print('!!!!! Hurray Found answer in ',i+1,' iterations')
                count = i+1
                break
            feedback = game.submit(sub)
            eq.update_feedback(feedback)
    except:
        print('Failed for :', ANSWER)
    return count

def bin_count(count):
    if count in count_stats.keys():
        count_stats[count] = count_stats[count] + 1
    else:
        count_stats[count] = 1
  
if __name__=='__main__':
    print('Get list of possible answers')
    length = 8
    eq = Equation(length)
    temp = eq.execute()
    count_stats = {}
    # answer_set = eq.equation_set
    answer_set = eq.equation_set
    # answer_set = answer_set[:10000]
    answer_set_itr = tqdm(answer_set)
    itr = 1
    total = len(answer_set)
    print('Answer set is ready. Equation Count:', total)
    with Pool(15) as p:
        counts = list(p.map(test_game, answer_set_itr))
    # counts = list(zip(*map(test_game, answer_set)))
        # outlier = counts.index(7)
    # print(answer_set[outlier])
    try:
        outlier = counts.index(7)
        print(answer_set[outlier])
    except:
        print('No entries for count=7')
    try:
        outlier = counts.index(8)
        print(answer_set[outlier])
    except:
        print('No entries for count=8')
    counts_itr = tqdm(counts)
    # print('Collating count stats')
    # # with Pool(20) as p:
    # #     p.map(bin_count, counts)
    for count in counts_itr:
        if count in count_stats.keys():
            count_stats[count] = count_stats[count] + 1
        else:
            count_stats[count] = 1
            
    print('Test Complete.\nCount Stats:', count_stats)