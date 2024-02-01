# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    from game import Directions
    North = Directions.NORTH
    East = Directions.EAST
    South = Directions.SOUTH
    West = Directions.WEST
    answer = []
    currentSimState = []
    explored = [problem.getStartState()]
    stack = util.Stack()
    parent = {}

    
    
    """
    print(f"\nexplored: {explored}")

    print("\nStart:", problem.getStartState())
    print("\nIs the start a goal?", problem.isGoalState(problem.getStartState()))
    print("\nStart's successors:", problem.getSuccessors(problem.getStartState()))


    
    print("\nfringe: ", fringe)

    currentSimState = fringe[0][0]
    print("\nIs the currentSimState a goal?", problem.isGoalState(currentSimState)
    print("\nSimulate South:", problem.getSuccessors(fringe[0][0]))
    """
    start = problem.getStartState()
    stack.push(start)
    while stack:
        currentSimState = stack.pop()

        print(f"\n Goal{currentSimState}? {problem.isGoalState(currentSimState)}\n")
        if problem.isGoalState(currentSimState):
            print(f"\n Goal Found \n")
            path = [currentSimState]
            break


        print(f"\n get getSuccessors  : {currentSimState}\n")
        fringe = problem.getSuccessors(currentSimState)
        for neighborState in fringe:
            print(f"\nneighbor: {neighborState}")
            if neighborState[0] not in explored:
                print(f"\n new state activated \n")
                parent[neighborState[0]] = currentSimState
                explored.append(neighborState[0])
                stack.push(neighborState[0])

    print(f"\n {parent}")

    while path[-1] != start:
        path.append(parent[path[-1]])


    path = list(reversed(path))
    print(f"\npath: {path}")

    for i in range(len(path) - 1):
        

        current_item = path[i]
        next_item = path[i + 1]
        
        if current_item[0] == next_item[0] + 1:
            answer.append(West)
        elif current_item[0] == next_item[0] - 1:
            answer.append(East)
        elif current_item[1] == next_item[1] + 1:
            answer.append(South)
        elif current_item[1] == next_item[1] - 1:
            answer.append(North)
        print(f"\ncurrent: {current_item} next: {next_item} answer: {answer[-1]}")
    return answer

    """ psuedo code for DFS

    while stack is not empty:
        currentSimState = util.pop(stack)

        if problem.isGoalState(currentSimState):
            path = [end]
            break
        
        for each neighborState in fringe:
            if neighborState is not in explored:
                parent[neighbor] = currentSimState
                explored.append(neighbor)
                util.push(neighbor)

    
    while path[-1] != start:
        path.append(parent[path[-1]])

    for state in list(reversed(path)):
        answer = state[1]
    return answer

        """


    print("")
    return answer
    

    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
