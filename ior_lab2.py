# -*- coding: utf-8 -*-
"""IOR_lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13WmGpHTUGnq5Mv3zOm6NqbdkLyKE-FAs
"""

import numpy as np
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

"""##2-APPROX"""

def greed(capacity, weights, prices):
    global count_0
    sorted_indices = sorted(range(len(prices)), key=lambda k: prices[k])
    knapsack = [0 for i in range(len(prices))]
    remaining_capacity = capacity
    profit = 0
    for i in reversed(sorted_indices):
        count_0 += 1
        if weights[i] <= remaining_capacity:
            profit += prices[i]
            knapsack[i] = 1
            remaining_capacity -= weights[i]
    return profit, knapsack, remaining_capacity

def quality_greed(capacity, weights, prices):
    global count_0
    profit = 0
    quality = [round(prices[i]/weights[i]) for i in range(len(prices))]
    sorted_indices = sorted(range(len(quality)), key=lambda k: quality[k])
    knapsack = [0 for i in range(len(prices))]
    remaining_capacity = capacity
    
    for i in reversed(sorted_indices):
        count_0 += 1
        if weights[i] <= remaining_capacity:
            profit += prices[i]
            knapsack[i] = 1
            remaining_capacity -= weights[i]
    return profit, knapsack, remaining_capacity


def two_approx(capacity, weights, prices):
    global count_0
    count_0 = 0
    gr_cost, gr_knapsack, gr_rm_capacity = greed(capacity, weights, prices)
    qgr_cost, qgr_knapsack, qgr_rm_capacity = quality_greed(capacity, weights, prices)
    if gr_cost > qgr_cost:
        return gr_cost, gr_knapsack, count_0, capacity - gr_rm_capacity
    else:
        return qgr_cost, qgr_knapsack, count_0, capacity - qgr_rm_capacity

"""##Branches/Borders"""

from scipy.optimize import linprog
count = 0

def new_node(prices_m, A_ub, b_ub, A_eq, b_eq, best_opt):
    global best_items
    global count_1
    res = linprog(prices_m, A_ub, b_ub, A_eq, b_eq, bounds=(0, 1))

    opt = -res['fun']
    items = [round(x, 3) for x in res['x']]

    #Ветвление происходит пока Relaxation soluion не целое и больше текущего лучшего
    if opt <= best_opt[0]:
        return
    for i in range(len(items)):
        
        if not items[i].is_integer():
            count_1 += 1
            A_eq_tmp = A_eq.copy()
            b_eq_tmp = b_eq.copy()
            A_eq_tmp.append([0 for x in range(len(items))])
            A_eq_tmp[-1][i] = 1
            b_eq_tmp.append(1)
            new_node(prices_m, A_ub, b_ub, A_eq_tmp, b_eq_tmp, best_opt)
            b_eq_tmp[-1] = 0
            new_node(prices_m, A_ub, b_ub,A_eq_tmp, b_eq_tmp, best_opt)
            return
    if opt > best_opt[0]:
        best_opt[0] = opt
        best_items = items
    return


def branches_borders(capacity, weights, prices):
    global count_1
    count_1 = 0

    prices_m = [-x for x in prices] #Для решения обратной задачи
    A_ub = [weights]
    b_ub = [capacity]
    A_eq = [[0 for x in range(len(weights))]]
    b_eq = [0]
    best_opt = [-1]

    new_node(prices_m, A_ub, b_ub, A_eq, b_eq, best_opt)
    total_price = 0
    total_weight = 0
    items = [int(best_items[i]) for i in range(len(best_items))]
    for i in range(len(items)):
        if items[i] == 1:
            total_price += prices[i]
            total_weight += weights[i]
    return total_price, total_weight, items, count_1

"""##Backpack dynamic"""

def backpack_dynamic(capacity, weight, cost):    # на весах
    count = 0
    n = len(weight)
    bag = [[0] * (capacity + 1) for _ in range(n + 1)]

    for k in range(1, n+1):
        for j in range(1, capacity+1):
            count += 1
            if j >= weight[k-1]:   # weight[k-1], cost[k-1] - т.к. в weight и cost нет первого нулевого элемента, значит индекс k в bag соответствует k-1 в weight и cost
                bag[k][j] = max(bag[k - 1][j], bag[k - 1][j - weight[k-1]] + cost[k-1])
            else:
                bag[k][j] = bag[k - 1][j]

    # находим, какие предметы брать
    res_weight = 0  # для итогового веса рюкзака
    result_id = [0] * n  # id предметов
    tmp = capacity
    for i in range(n, 0, -1):
        if bag[i][tmp] != bag[i - 1][tmp]:
            res_weight += weight[i-1]
            result_id[i-1] = 1
            tmp -= weight[i-1]

    return bag[n][capacity], res_weight, result_id, count



import os
import time
import pandas as pd
import matplotlib.pyplot as plt


def for_all_files():
    data = os.listdir('data')
    for dir_ in data:
        with open(f'data/{dir_}/{dir_}_c.txt', 'r') as c:
            capacity = int(c.read())     # вместимость рюкзака
        with open(f'data/{dir_}/{dir_}_p.txt', 'r') as p:
            p = p.read().split()
            cost = [int(i) for i in p]     # стоимость предметов
        with open(f'data/{dir_}/{dir_}_s.txt', 'r') as s:
            opt_w = s.read().split()
            opt_w = [int(i) for i in opt_w]     # optimal selection of weights
        with open(f'data/{dir_}/{dir_}_w.txt', 'r') as w:
            w = w.read().split()
            weight = [int(i) for i in w]     # вес предметов
        times_res = [0, 0, 0]
        counts_res = [0, 0, 0]
        weights_res = [0, 0, 0]
        costs_res = [0, 0, 0]
        ids_res = [[], [], []]
        #print(capacity)
        #print(weight)
        #print(cost)
        #print(opt_w)
        #n = len(weight)         #  количество предметов
        start0 = time.time()
        costs_res[0], weights_res[0], ids_res[0], counts_res[0] = backpack_dynamic(capacity, weight, cost)    #  ДП на весах
        stop0 = time.time()
        times_res[0] = stop0-start0
        start1 = time.time()
        costs_res[1], weights_res[1], ids_res[1], counts_res[1] = branches_borders(capacity, weight, cost)
        stop1 = time.time()
        times_res[1] = stop1-start1
        start2 = time.time()
        costs_res[2], ids_res[2], counts_res[2], weights_res[2] = two_approx(capacity, weight, cost)
        stop2 = time.time()
        times_res[2] = stop2 - start2
        df=pd.DataFrame({"Algorithm":['Dynamic', 'Branches_borders', '2-approx'], "Time(s)":times_res, "Counter": counts_res, "Total Weight": weights_res, "Total Cost": costs_res, 
                         "Backpack accepted": ids_res, "Backpack opt": [opt_w, opt_w, opt_w]}, index=['','',''])
        with pd.option_context('display.max_rows', None, 'display.max_columns', 500):
          print(f'----------------------------{dir_}----------------------------')
          #print("--------------------------------------------------------------")
          display(df)

def main():
    for_all_files()

if __name__ == '__main__':
    main()

rmdir data/.ipynb_checkpoints

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# jupyter nbconvert --to html /content/IOR_lab2.ipynb

