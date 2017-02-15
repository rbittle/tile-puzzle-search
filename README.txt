Name:
    Riley Walters Bittle
    rdw150230

Source Files:
    search.py

Instructions to run:
    The file can be run like:

        python3 search.py [-cost] <BFS|DFS|UCS|GS|A-star> <inputfile>

        or

        ./search.py [-cost] <BFS|DFS|UCS|GS|A-star> <inputfile>

    The file has a help command, -h or --help, that will print the above text.

Platform:
    Developed on Linux using Python 3.6.0

Problems:
    I faced many problems while developing the implementation and solution to making the puzzle search algorithm.
    My first main challange was finding a way to properly represent the search data in code. One initial idea was to have each node, or state such as "WxB" be an instance of a node class. I decided this would be too slow to implement, so instead I represented each node as a tuple, that contained the total path cost, the string representation, the former string representation, and the character that was moved from the former to current state. This data structure more represents a change from one state to the next instead of a single state in general, which I believe will run much faster.
    The reason the state transition tuple contains so much information is because of the need to backtrack the search path in order to print out the optimal path from start to finish, and to properly calculate and accumulate costs.
    The backtracking was by far the hardest problem. Initially I didn't keep track of a node's parent, so I was unable to retrace my steps at all. My solution to this is way more complicated than needed, but I think it makes the algorithm much faster as the search space increases. The solution was to create a lookup table that kept track of each state's parents, so that I can walk back up the path using each node's looked-up parents. This works flawlessly for all searches except for depth first search, where the solution may not be optimal, because DFS is not a complete search.
    The implementation of python's queue structures might have also changed the order in which DFS looks through the tree, but it returns a similar solution to the given examples, and always provides a valid solution. All other search types provide the optimal search path.
