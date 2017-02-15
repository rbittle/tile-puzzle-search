#! /bin/python3

import argparse
import re
from queue import Queue, PriorityQueue, LifoQueue

# command line argument parsing
parser = argparse.ArgumentParser()

# Adds cost, search type, and input file command line arguments as described in the document.
parser.add_argument("-cost", action="store_true", help="Uses the furthest-move-optimal cost weights.")
parser.add_argument("search_type", help="Can be: BFS, DFS, UCS, GS, A-star")
parser.add_argument("input_file", help="File containing the initial game state. This will be validated before being ran. The program assumes there will be at least one white square and one black square.")

args = parser.parse_args()


class TileGame:
    ''' This class is a persistant instance of a game.
    It keeps track of the search type, search space,
    and all expanded nodes.

    Running search() on an instance of the TileGame will preform a search
    given the inputs specified at the command line.
    '''

    # initializes the object using the command line arguments
    def __init__(self, initial_state): 
        self.initial_state = initial_state
        self.visited = []
        self.opened = {}

        if args.search_type.upper() == "BFS":
            self.q = Queue()
        elif args.search_type.upper() == "DFS":
            self.q = LifoQueue()
        else: # UCS, GS, A-star
            self.q = PriorityQueue()
    
    # Gets all available movements given a state, and filters out all previously
    # explored nodes in the current search.
    def available(self, state_tup):
        # passing sring to get possible states
        possible_states = next_states(state_tup)
        state = state_tup[1]
        # filter out already visited states
        valid_states = [state for state in possible_states if state[1] not in self.visited]
        return valid_states 

    # Once the solution is found, this function traces the parents to create
    # a formatted output text.
    def deconstruct_solution(self, solution_state):

        ''' test printing
        for v in self.opened.values():
            print(v, test_solution(v[1]) != None)
        '''

        current = solution_state
        # initialize step counter and path printer
        step = 0
        path = LifoQueue()

        path.put(current)
        # While the currently looked at state is not the initial state, add it to the
        # end path, then use the lookup table to find the states parent, and try again.
        while self.opened[current[1]] != "start":
            current = self.opened[current[1]]
            path.put(current)

        # Once the path is costructed, print the path using the format described
        # in the specification document.
        while not path.empty():
            node = path.get()
            if node[3] == "start":
                print("Step "+str(step)+":  "+node[1])
            else:
                if args.cost:
                    print("Step "+str(step)+":  move "+str(node[3])+" "+node[1]+" (c="+str(print_cost(node))+")")
                else:
                    print("Step "+str(step)+":  move "+str(node[3])+" "+node[1])
            step += 1
        
    def search(self):
        # Start by inserting a formatted initial state node
        self.q.put((0, self.initial_state, "start", "start"))
        # Add the start to the opened states, formatted for end path retrieval.
        self.opened[self.initial_state] = "start"
        # print("Start: "+self.initial_state)
        
        # While the queue structure still has nodes, search for the end state.
        while not self.q.empty():
            current_state = self.q.get()
            # add current state to visited states.
            self.visited.append(current_state[1])
            # check if the state is the solution
            if test_solution(current_state[1]):
                # if solution found, print the solution path and stop iterating the search.
                #self.opened[current_state[1]] = "end"
                self.deconstruct_solution(current_state)
                break

            # if the state is not a solution, get the available states and add them to the queue.
            for next_state in self.available(current_state):
                self.q.put(next_state)
                # To get the final path, construct a parent lookup table
                # assume first accessed instance of node is least cost
                # should work for all complete search algorithms (i.e. not DFS)
                if next_state[1] not in self.opened:
                    self.opened[next_state[1]] = current_state


def test_valid(state):
    # checks if the string contains a series of w, b, and one x
    valid_test = re.compile(r"^[wWbB]*[xX][wWbB]*$")
    # return truthy match if the string is valid
    return valid_test.match(state)

def test_solution(state):
    ''' Test_solution function uses regex to check if a state string is a solution.'''
    # checks if the string is all black then one blank then all white
    solution_test = re.compile(r"^[bB]+[xX][wW]+$")
    # return truthy match if the string is a solution state
    return solution_test.match(state)

def heuristic(state):
    ''' This function calculates the heuristic cost for a given state.'''
    x_index = state.index('x')
    # creates an array based on the input string
    chars = list(state.upper())

    cost = 0
    # counts the number of W's before the 'x'
    for i in range(0, x_index):
        if chars[i] is "W":
            cost += 1

    # counts the number of B's before the 'x'
    for j in range(x_index+1, len(chars)):
        if chars[j] is "B":
            cost += 1

    return cost

def print_cost(state_tup):
    ''' This function returns the cost of making a move
    for printing during the path reconstruction. 
    The actual costs used during the search are modified in order
    to use the same logic, but keeps it lower-is-better to re-use code'''
    moved = state_tup[3] # index of moved character
    x_pos = state_tup[2].lower().index('x') # position of the empty square in parent state
    return abs(moved - x_pos)

def swap_x(state_tup, i):
    ''' This function swaps the tile at index i, and returns a state tuple that includes
    the cost, state as a string, parent state as a string, and index that was swapped
    to achieve the new state'''

    state = state_tup[1] # string of state

    i_char = state[i] # character that is being swapped
    x_pos = state.lower().index('x') # position of the 'x' tile

    # initialize new cost value depending if the cost flag was used
    if args.cost:
        cost = len(state) - abs(i - x_pos)
    else:
        cost = 1

    # swap the two characters in a weird way because python's immutable strings
    new_state = state.replace('x', i_char, 1)
    new_state = list(new_state) # array of chars
    new_state[i] = 'x'
    new_state = ''.join(new_state)

    # if using a heuristic based search, add or set the heuristic cost
    if args.search_type == "GS":
        # greedy search only uses the heuristic search
        cost = heuristic(new_state)
    elif args.search_type == 'A-star':
        # A-star search adds the heuristic search to the movement cost
        cost += heuristic(new_state)

    # new state is a tuple (cost, state, prev_state, swapped index)
    return (cost + state_tup[0], new_state, state, i)

def next_states(state_tup):
    ''' gets an array of all possible states one move from the start state, and includes the cost'''
    state = state_tup[1] # state as string
    state_array = list(state) # state as array of chars
    
    next_states = []

    # for each tile that is not the empty tile,
    # swap the tile with the 'x' and add it to the array of possible states.
    for i, tile in enumerate(state_array):
        if tile is 'x': # ignore 'x' tile
            continue 
        new_state = swap_x(state_tup, i)
        next_states.append(new_state)

    return next_states       


# logic for running the program from the command line
if __name__ == "__main__":
    f = open(args.input_file, 'r') # assume file is valid (no exception checking)
    puzzle = f.read().strip() # grab the initial state as a string, trimming any whitespace

    # check if the puzzle is valid
    if not test_valid(puzzle):
        print("Puzzle not valid: "+puzzle)
    else:
        # create the game object and run the search
        game = TileGame(puzzle)
        game.search()
