# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # for each iteration
        for _ in range(self.iterations):

            # get all the states
            states = self.mdp.getStates()
            tempValues = util.Counter()

            # for each state get its max Q value and save to counter
            for s in states:
                maxVal = -1_000_000
                for a in self.mdp.getPossibleActions(s):
                    qValue = self.computeQValueFromValues(s, a)
                    maxVal = max(maxVal, qValue)
                    tempValues[s] = maxVal

            self.values = tempValues


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)

        # get each possible state and its probability from the current state
        for next_state, prob in transition_states:

            # get the reward for the transition
            reward = self.mdp.getReward(state, action, next_state)

            # calculate the Q value
            q_value += prob * (reward + self.discount * self.values[next_state])

        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possible_actions = self.mdp.getPossibleActions(state)
        
        max_reward = (-1_000_000, 'None')
        
        for action in possible_actions:

            # get the next possible states
            future = self.mdp.getTransitionStatesAndProbs(state, action)
            reward = 0

            for transition in future:
                nextState, prob = transition
                reward += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))

            if reward > max_reward[0]:
                max_reward = (reward, action)

        return max_reward[1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        priorityQueue = util.PriorityQueue()

        predecessors = {state: set() for state in self.mdp.getStates()}
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for next_state, _ in self.mdp.getTransitionStatesAndProbs(state, action):
                        predecessors[next_state].add(state)

        # for each state that is not terminal
        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):

                # get the max Q value
                maxQ =  float('-inf')
                for a in self.mdp.getPossibleActions(s):
                    q_value = self.computeQValueFromValues(s, a)
                    if q_value > maxQ:
                        maxQ = q_value

                # difference in absolute value of the current value and the max Q value
                # print(f"diff: abs({self.values[s]} - {maxQ})")
                diff = abs(self.values[s] - maxQ)

                # add to the queue
                # print(f"adding {s}, {diff}")
                priorityQueue.push(s, diff)
                
        # For iteration in 0, 1, 2, ..., self.iterations - 1, do
        for k in range(0, self.iterations-1):

            # if queue is empty terminate
            if priorityQueue.isEmpty():
                break

            # pop s off priority queue
            s = priorityQueue.pop()

            # if its not terminal update its value TODO check if this is correct
            if not self.mdp.isTerminal(s): 
                maxQ = float('-inf')  
                for action in self.mdp.getPossibleActions(s):
                    q_value = self.computeQValueFromValues(s, action)
                    maxQ = max(maxQ, q_value) 

                self.values[s] = maxQ 

            # for each predecessor of s (p = (s, action))
            for p in predecessors[s]:
                # get the max Q value
                maxQ = float('-inf')
                for a in self.mdp.getPossibleActions(p):
                    
                    q_value = self.computeQValueFromValues(p, a)

                    if q_value > maxQ:
                        maxQ = q_value

                diff = abs(self.values[p] - maxQ)

                if diff > self.theta:
                    priorityQueue.update(p, -diff)

    

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)

        for next_state, prob in transition_states:
            reward = self.mdp.getReward(state, action, next_state)
            q_value += prob * (reward + self.discount * self.values[next_state])

        return q_value

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possible_actions = self.mdp.getPossibleActions(state)
        
        max_reward = (-1_000_000, 'None')
        
        for action in possible_actions:

            # get the next possible states
            future = self.mdp.getTransitionStatesAndProbs(state, action)
            reward = 0

            for transition in future:
                nextState, prob = transition
                reward += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))

            if reward > max_reward[0]:
                max_reward = (reward, action)

        return max_reward[1]