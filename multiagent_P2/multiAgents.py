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

        # this for loop it outside to track the moves associated with the values
        for action in gameState.getLegalActions(0):


            # if pacman makes the first move what is the reward from the rest of the moves
            newReward = self.minimaxFunc(gameState.generateSuccessor(self.index, action), self.depth, self.index + 1)

            # track the best reward and move
            if newReward > reward:
                # print(f"{action}: {newReward}")
                reward = newReward
                bestAction = action


        return bestAction

    def minimaxFunc(self, gameState, depth, index):

        # makes sure index cycles
        index = index % gameState.getNumAgents()

        # if tree is in terminal state
        if gameState.isWin() or gameState.isLose() or depth == 0:

            return self.evaluationFunction(gameState)

        # go to next depth after the last agent goes
        if index+1 == gameState.getNumAgents():
            depth -= 1

        # maximizing player
        if index == 0:
            # make no choice extrememly expenseive
            bestValue = -1_000_000

            # go through each legal move
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue = self.minimaxFunc(gameState.generateSuccessor(index, move), depth, index+1)
                bestValue = max(bestValue, newValue)

            return bestValue


        # minimizing player
        else:
            # make no choice extremely expensive
            bestValue = 1_000_000
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue = self.minimaxFunc(gameState.generateSuccessor(index, move), depth, index+1)
                bestValue = min(bestValue, newValue)

            return bestValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        reward = Alpha = -1_000_000
        Beta = 1_000_000

        # if pacman makes the first move what is the reward from the rest of the moves
        value, action = self.minimaxFuncAB(gameState, self.depth, self.index, Alpha, Beta)

        return action

    def minimaxFuncAB(self, gameState, depth, index, Alpha,Beta):

        # cycles agents and updates depth
        if index >= gameState.getNumAgents():
            depth -= 1
            index = 0

        # if tree is in terminal state
        if gameState.isWin() or gameState.isLose() or depth == 0:
            newValue = self.evaluationFunction(gameState)

            # print(f"a{index}) alpha: {Alpha}, Beta: {Beta}, newValue: {newValue}")
            return newValue, None



        # maximizing player
        if index == 0:
            # make no choice extrememly expenseive
            bestValue = -1_000_000
            bestMove = ''

            # go through each legal move
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue, _ = self.minimaxFuncAB(gameState.generateSuccessor(index, move), depth, index+1, Alpha, Beta)

                # update the value and the best move for pacman
                if newValue > bestValue:
                    bestValue = newValue
                    bestMove = move
                
                # if true prune
                if bestValue > Beta:

                    # print(f"a{index}) alpha: {Alpha}, Beta: {Beta}, val: {bestValue} move: {move}")
                    return bestValue, bestMove

                Alpha = max(Alpha, bestValue)

            # print(f"a{index}) alpha: {Alpha}, Beta: {Beta}, val: {bestValue} move: {move}")
            return bestValue, bestMove


        # minimizing player
        else:
            # make no choice extremely expensive
            bestValue = 1_000_000
            for move in gameState.getLegalActions(index):

                # get next state. If its terminal it returns here
                newValue, _ = self.minimaxFuncAB(gameState.generateSuccessor(index, move), depth, index+1, Alpha, Beta)
                bestValue = min(bestValue, newValue)
                
                # if true prune
                if bestValue < Alpha:
                    # print(f"a{index}) alpha: {Alpha}, Beta: {Beta}, val: {bestValue}")
                    return bestValue, None

                Beta = min(Beta, bestValue)

            # print(f"a{index}) alpha: {Alpha}, Beta: {Beta}, val: {bestValue}")
            return bestValue, None


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

        # Track the maximum utility for pacman agent
        maxUtil = -1_000_000

        for action in gameState.getLegalActions(0):
            # Get the utility of the current action
            currUtil = self.getValue(gameState.generateSuccessor(self.index, action), self.depth, self.index + 1)

            # Update the maximum utility, and track its associated action
            if currUtil > maxUtil:
                maxUtil = currUtil
                bestAction = action

        return bestAction

    # Return a value in the expectimax tree
    def getValue(self, gameState: GameState, depth, index):
        # Allow index to wrap around (index in (Z/indexZ))
        index = index % gameState.getNumAgents()

        # Get value at terminal state
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        # Go to the next depth once all agents at the current depth have gone
        if index + 1 == gameState.getNumAgents():
            depth -= 1

        # Pacman agent
        if index == 0:
            value = -1_000_000
            # Loop through all legal actions for the Pacman agent
            for action in gameState.getLegalActions(index):
                # Find the max value between the current value and the value of the successor state
                value = max(value, self.getValue(gameState.generateSuccessor(index, action), depth, index+1))
            return value
        # Ghost agent
        else:
            value = 0
            # Loop though all legal actions for the current ghost agent
            for action in gameState.getLegalActions(index):
                # Probability for a ghost choosing one of its legal moves is equally random
                prob = 1.0 / len(gameState.getLegalActions(index))
                value += prob * self.getValue(gameState.generateSuccessor(index, action), depth, index+1)
            return value

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
