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
from game import Directions
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
    answer = []
    explored = [problem.getStartState()]
    stack = util.Stack()
    parent = {}
    start = problem.getStartState()
    
    stack.push(start)
    while stack:
        currentSimState = stack.pop()
        explored.append(currentSimState)

        # break if you find the goal
        if problem.isGoalState(currentSimState):
            path = [currentSimState]
            break

        # gets the fringe
        fringe = problem.getSuccessors(currentSimState)

        # loops through the fringe
        for fringeState in fringe:

            # if a state in the fringe is not explored & save corresponding info
            if fringeState[0] not in explored:
                parent[fringeState[0]] = [currentSimState, fringeState[1]]
                
                stack.push(fringeState[0])
                # these are not explored yet
    
    # once you have found the goal get the path from finish to start
    while path[-1] != start:
        answer.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])

    # reverse list to be start to finish
    answer = list(reversed(answer))

    return answer


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    answer = []
    explored = []
    queue = util.Queue()
    parent = {}
    start = problem.getStartState()
    
    queue.push(start)
    while queue:

        # gets next node as long as its not explored
        currentSimState = queue.pop()
        while currentSimState in explored:
            currentSimState = queue.pop()
        explored.append(currentSimState)


        # break if you find the goal
        if problem.isGoalState(currentSimState):
            path = [currentSimState]
            break

        # gets the fringe
        fringe = problem.getSuccessors(currentSimState)

        # loops through the fringe
        for fringeState in fringe:
            
            # explored doesnt get updated until fringe duplicates are added
            if fringeState[0] not in explored:

                # only give node a parent if it does have one
                if fringeState[0] not in parent:
                    parent[fringeState[0]] = [currentSimState, fringeState[1]]

                # and next layer to queue
                queue.push(fringeState[0])

    # once you have found the goal get the path from finish to start
    while path[-1] != start:
        answer.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])

    # reverse list to be start to finish
    answer = list(reversed(answer))

    return answer

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    answer = []
    explored = []
    queue = util.PriorityQueue()
    parent = {}
    start = problem.getStartState()
    queue.push(start, 0)
    currentCost = 0
    while queue:

        # gets next node as long as its not explored
        currentSimState = queue.pop()
        while currentSimState in explored:
            currentSimState = queue.pop()
        explored.append(currentSimState)

        # break if you find the goal
        if problem.isGoalState(currentSimState):
            path = [currentSimState]
            break

        # gets the fringe
        fringe = problem.getSuccessors(currentSimState)

        # loops through the fringe
        for fringeState in fringe:

            # explored doesnt get updated until fringe duplicates are added
            if fringeState[0] not in explored:

                # gets the cost of the current node
                if currentSimState in parent:
                    currentCost = parent[currentSimState][2]

                # add the cost of the node in the parent dictionary. Format as follows
                # {child: ["childs parent", "move from parent to child", "cost to get to child from start"]}
                newCost = fringeState[2] + currentCost
                if fringeState[0] not in parent or parent[fringeState[0]][2] > newCost:
                    parent[fringeState[0]] = [currentSimState, fringeState[1], newCost]
                else:
                    parent[fringeState[0]][2] += currentCost
                

                # and next layer to queue
                queue.push(fringeState[0], fringeState[2] + currentCost)



    # once you have found the goal get the path from finish to start
    while path[-1] != start:
        print(f"\n yes: {parent[path[-1]][1]}")
        answer.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])

    # reverse list to be start to finish
    answer = list(reversed(answer))

    return answer

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    answer = []
    explored = []
    queue = util.PriorityQueue()    # Queue to keep track of node with lowest cost
    parent = {} # {'child': ['parent of child', 'action from parent to child', 'cost from start']}
    start = problem.getStartState()
    queue.push(start, heuristic(start, problem))
    currentCost = 0

    while queue:
        # gets next node as long as its not explored
        currentSimState = queue.pop()
        while currentSimState in explored:
            currentSimState = queue.pop()
        explored.append(currentSimState)

        # break if you find the goal
        if problem.isGoalState(currentSimState):
            path = [currentSimState]
            break

        # gets the fringe
        fringe = problem.getSuccessors(currentSimState)

        # loops through the fringe
        for fringeState in fringe:
            # explored doesnt get updated until fringe duplicates are added
            if fringeState[0] not in explored:

                # gets the cost of the current node
                if currentSimState in parent:
                    currentCost = parent[currentSimState][2]

                # add the cost of the node in the parent dictionary. Format as follows
                # {child: ["childs parent", "move from parent to child", "cost to get to child from start"]}
                newCost = fringeState[2] + currentCost    # Get the total cost up to the current node (g value)
                h = heuristic(fringeState[0], problem)  # Get the heuristic value for the current node
                # If this child is not in the parent list add it
                # Or, if it is in the parent but the new cost is less than the old one, update this tuple
                if fringeState[0] not in parent or parent[fringeState[0]][2] > newCost:
                    parent[fringeState[0]] = [currentSimState, fringeState[1], newCost]
                
                # and next layer to queue
                queue.push(fringeState[0], newCost + h)   # Add state to priority queue with priority g + h (cost to that point + heuristic)



    # once you have found the goal get the path from finish to start
    while path[-1] != start:
        print(f"\n yes: {parent[path[-1]][1]}")
        answer.append(parent[path[-1]][1])
        path.append(parent[path[-1]][0])

    # reverse list to be start to finish
    answer = list(reversed(answer))

    return answer

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
