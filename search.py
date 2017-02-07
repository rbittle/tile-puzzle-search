#! /bin/python3

import argparse
import re
from queue import Queue, PriorityQueue, LifoQueue

# command line argument parsing
parser = argparse.ArgumentParser()

parser.add_argument("-cost", action="store_true")
parser.add_argument("search_type")
parser.add_argument("input_file")

args = parser.parse_args()



class TileGame:
    def __init__(self, initial_state): 
        self.initial_state = initial_state
        self.visited = []

        if args.search_type is "BFS":
            self.q= Queue()
        elif args.search_type is "DFS":
            self.q= LifoQueue()
        else:
            self.q = PriorityQueue()
    
    def search(self):
        self.q.put((0, self.initial_state))
        
        #test
        first = self.q.get()
        print(next_states(first[1]))
        #endtest

    def available(self):
        pass

def test_valid(state):
    # checks if the string contains a series of w, b or x
    test = re.compile(r"^[wWbB]*[xX][wWbB]*$")
    # return true if the string is valid
    return test.match(state)

def swap_x(state, i):
    i_char = state[i]
    x_pos = state.index('x')

    if args.cost:
        cost = abs(i - x_pos)
    else:
        cost = 1

    new_state = state.replace('x', i_char, 1)
    new_state = list(new_state) # array of chars
    new_state[i] = 'x'
    new_state = ''.join(new_state)

    return (cost, new_state)

def next_states(state):
    # gets an array of possible states possible one move from the start state, including the cost
    state_array = list(state)
    
    next_states = []

    for i, tile in enumerate(state_array):
        if tile is 'x':
            continue
        # new_state is a tuple (cost, state)
        new_state = swap_x(state, i)
        next_states.append(new_state)

    return next_states       



#TESTING#

test = TileGame("WBxW")
test.search()
