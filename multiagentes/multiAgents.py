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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]        


        distance = []
        foodList = currentGameState.getFood().asList()
        pacmanPos = list(successorGameState.getPacmanPosition())

        if action == 'Stop':
            return -float("inf")

        for ghostState in newGhostStates:
            if ghostState.getPosition() == tuple(pacmanPos) and ghostState.scaredTimer is 0:
                return -float("inf") 
    
        for food in foodList:
            x = -1*abs(food[0] - pacmanPos[0])
            y = -1*abs(food[1] - pacmanPos[1])
            distance.append(x+y) 
    
        return max(distance)
    
def scoreEvaluationFunction(currentGameState):
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
    #def min(state):
    #def max(state):
    def getAction(self, gameState):
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
        """
        res = self.value(gameState, 0)
        return res[0]

    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxFunc(gameState, depth)
        else:
            return self.minFunc(gameState, depth)

    def minFunc(self, gameState, depth):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.value(succ, depth+1)
            if res[1] < min_val[1]:
                min_val = (action, res[1])
        return min_val

    def maxFunc(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.value(succ, depth+1)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
        return max_val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        res = self.value(gameState, 0, -float("inf"), float("inf"))
        return res[0]

    def value(self, gameState, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            # pacman
            return self.maxFunc(gameState, depth, alpha, beta)
        else:
            # ghosts
            return self.minFunc(gameState, depth, alpha, beta)

    def minFunc(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.value(succ, depth+1, alpha, beta)
            if res[1] < min_val[1]:
                min_val = (action, res[1])
            if min_val[1] < alpha:
                return min_val
            beta = min(beta, min_val[1])
        return min_val

    def maxFunc(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.value(succ, depth+1, alpha, beta)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
            if max_val[1] > beta:
                return max_val
            alpha = max(alpha, max_val[1])
        return max_val