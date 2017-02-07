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
        self.opened = []

        if args.search_type.upper() == "BFS":
            self.q = Queue()
        elif args.search_type.upper() == "DFS":
            self.q = LifoQueue()
        else: # UCS, GS, A-star
            self.q = PriorityQueue()
    
    def available(self, state):
        # passing sring to get possible states
        possible_states = next_states(state)
        # filter out already visited states
        valid_states = [state for state in possible_states if state[1] not in self.visited]
        return valid_states 

    def deconstruct_solution(self, solution_state):
        parents = {}
        for node in self.opened:
            parents[node[1]] = next((parent for parent in self.opened if parent[1] == node[2]), "start")

        current = solution_state
        step = 0
#TODO
        while current != 'start':
            # print("Step "+str(step)+":  move "+str(current[3])+" "+current[1])
            print(current)
            step += 1
            current = parents[current[2]]
        print(current)

    def search(self):
        self.q.put((0, self.initial_state, "start", -1))
        print("Start: "+self.initial_state)
        
        while not self.q.empty():
            current_state = self.q.get()
            self.opened.append(current_state)
            print("Visiting: " + current_state[1] + " from " + str(current_state[2]))
            # add current state to visited states
            self.visited.append(current_state[1])
            # check if the state is the solution
            if test_solution(current_state[1]):
                print("Solution found\n")
                self.deconstruct_solution(current_state)
                break

            for next_state in self.available(current_state[1]):
                self.q.put(next_state)

        # add available states to queue


def test_valid(state):
    # checks if the string contains a series of w, b or x
    valid_test = re.compile(r"^[wWbB]+[xX][wWbB]+$")
    # return truthy match if the string is valid
    return valid_test.match(state)

def test_solution(state):
    # checks if the string is all black then one blank then all white
    solution_test = re.compile(r"^[bB]+[xX][wW]+$")
    # return truthy match if the string is a solution state
    return solution_test.match(state)

def heuristic(state):
    x_index = state.index('x')
    chars  = list(state.upper())

    cost = 0
    for i in range(0, x_index):
        if chars[i] is "W":
            cost += 1

    for j in range(x_index+1, len(chars)):
        if chars[j] is "B":
            cost += 1

    return cost

def swap_x(state, i):
    i_char = state[i]
    x_pos = state.index('x')

    cost = 0
    if args.cost:
        cost = abs(i - x_pos)
    else:
        cost = 1

    new_state = state.replace('x', i_char, 1)
    new_state = list(new_state) # array of chars
    new_state[i] = 'x'
    new_state = ''.join(new_state)

    if args.search_type == "GS":
        cost = heuristic(new_state)
    elif args.search_type == 'A-star':
        cost += heuristic(new_state)

    # new state is a tuple (cost, state, prev_state)
    return (cost, new_state, state, i)

def next_states(state):
    # gets an array of possible states possible one move from the start state, including the cost
    state_array = list(state)
    
    next_states = []

    for i, tile in enumerate(state_array):
        if tile is 'x':
            continue
        # new_state is a tuple (cost, state, prev_state)
        new_state = swap_x(state, i)
        next_states.append(new_state)

    return next_states       


if __name__ == "__main__":
    puzzle = "WxB"

    if not test_valid(puzzle):
        print("Starting state not valid")
    else:
        game = TileGame(puzzle)
        game.search()
