# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        # # print(f"legal: {legalMoves}\n scores: {scores}\n bestScores: {bestScore}\n bestIndices{bestIndices} \nchosenIndex:{chosenIndex}\n")
        #"Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        # Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [(ghostState.getPosition(), ghostState.scaredTimer) for ghostState in newGhostStates]

        dangerousSpots = []
        foodDistances = []
        ghostDistances = []
        penalty = 0
        minFood = 0.1

        # gets the distances to food
        foodSpots = newFood.asList()
        for food in foodSpots:
            foodDistances.append((manhattanDistance(newPos, food), newPos))

        # gets closest food
        if len(foodDistances) != 0:
            minFood = min(foodDistances)[0]        

        # gets distances to ghosts
        for ghost in newGhostStates:
            ghostDistances.append((manhattanDistance(newPos, ghost.getPosition()), newPos))

        # gets closest ghost
        minGhost = min(ghostDistances)[0]


        # gets areas where ghost could be
        for (x, y) in newScaredTimes:
             if y > 1:
                dangerSpot = x
                dangerousSpots.append(((dangerSpot[0]-1), dangerSpot[1]))
                dangerousSpots.append(((dangerSpot[0]+1), dangerSpot[1]))
                dangerousSpots.append(((dangerSpot[0]), dangerSpot[1]-1))
                dangerousSpots.append(((dangerSpot[0]), dangerSpot[1]+1))

        # punish bad decisions
        if newPos in dangerousSpots:
            penalty += 30 
        if action == 'Stop':
            penalty += 10



        return successorGameState.getScore() + 10/minFood + minGhost/10 - penalty

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        reward = -1_000_000

        for action in gameState.getLegalActions(0):

            # print(f"try {action} from: {gameState.getLegalActions(0)}")
            
            # if i make the first move what is the reward from the rest of the moves
            newReward = self.minimaxFunc(gameState.generateSuccessor(self.index, action), self.depth, self.index + 1)

           
            if newReward > reward:
                print(f"{action}: {newReward}")
                reward = newReward
                bestAction = action

        # action = self.minimaxFunc(gameState, self.depth, self.index)
        # print(f"final action {action} from {gameState.getLegalActions(0)}\n{str(gameState)}")

        return bestAction

    # i think the problem is assinging the prevois move to the current agent
    # need to call minimax for each move from start and only return the value

    def minimaxFunc(self, gameState, depth, index):

        index = index % gameState.getNumAgents()

        # if tree is in terminal state
        if gameState.isWin() or gameState.isLose() or depth == 0:

            return self.evaluationFunction(gameState)
            

        # maximizing player
        if index == 0:            
            bestValue = -1_000_000
            # go through each legal move
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue = self.minimaxFunc(gameState.generateSuccessor(index, move), depth-1, index+1)
                bestValue = max(bestValue, newValue)
                
                #testing
                #evalTupleList.append(newValue)

            # print(f"Pacman max {bestValue} at {depth} from {evalTupleList} legal: {gameState.getLegalActions()}\n")
            # print("**********************************************************\n")
            return bestValue


        # minimizing player
        else:
            bestValue = 1_000_000
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue = self.minimaxFunc(gameState.generateSuccessor(index, move), depth, index+1)
                bestValue = min(bestValue, newValue)

                #testing
                #evalTupleList.append(newValue)

            # print(f"agent{index} min at {depth}: ({bestValue} over {newValue})  from {evalTupleList} legal: {gameState.getLegalActions()}\n")
            # print("**********************************************************\n")
            return bestValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
