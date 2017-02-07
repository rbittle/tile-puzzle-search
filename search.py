import argparse
import re

'''
parser = argparse.ArgumentParser()

parser.add_argument("-cost", action="store_true")
parser.add_argument("search-type")
parser.add_argument("input-file")

args = parser.parse_args()
'''

class TileGame:
    def __init__(self, initial_state): 
        self.tiles = initial_state
        self.visited = []
    
def test_valid(state):
    # checks if the string contains a series of w, b or x
    test = re.compile(r"^([wWbBx]+)$")
    # return true if the string is valid
    return test.match(state)

def swap_x(state, i):
    i_char = state[i]
    new_state = state.replace('x', i_char, 1)
    new_state = new_state.split('')
    new_state[i] = 'x'
    new_state = ''.join(new_state)
    return new_state

def next(state):
    # gets an array of possible states possible one move from the start state, including the cost
    state_array = state.split('')
    
    next_states = []

    for i, tile in enumerate(state_array):
        if tile is 'x':
            continue
        # new_state is a tuple (state, cost)
        new_state = swap_x(state, i)
        if new_state[0] not in self.visited:
            next_states.append(new_state)

    return next_states       

print(swap_x("WWxB", 1))
