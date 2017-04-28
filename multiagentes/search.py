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

############################################################################
# Ep1 - Aluno: Eduardo Santos Costa
############################################################################

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    ############################################################################
    # getStartState -> Returns the start state for the search problem.
    # isGoalState -> True or false.
    # getSuccessors -> Return list of triples, (successor, action, stepCost).
    ############################################################################
    border = util.Stack()
    set_expanded = set()
    border.push((problem.getStartState(), [],0))
    while True:
        if border.isEmpty():
            return False
        state, action, stepcost = border.pop()
        if(state in set_expanded):
            continue
        set_expanded.add(state)
        if problem.isGoalState(state):
            return action
        for successor, action_x, cost in problem.getSuccessors(state):
            border.push((successor, action+[action_x], cost))
    return None
    #==================================PRONTO==================================#
def breadthFirstSearch(problem):

    ############################################################################
    # getStartState -> Returns the start state for the search problem.
    # isGoalState -> True or false.
    # getSuccessors -> Return list of triples, (successor, action, stepCost).
    ############################################################################
    
    border = util.Queue()
    set_expanded = []
    border.push((problem.getStartState(), [], 0))
    while True:
        if border.isEmpty():
            return False
        state, action, stepcost = border.pop()
        if problem.isGoalState(state):
            return action
        if state not in set_expanded:
            set_expanded.append(state)
            for successor, action_x, cost in problem.getSuccessors(state):
                border.push((successor, action+[action_x], cost))
    return None
    #==================================PRONTO==================================#
def dls(problem, depth):
    # dlf -> busca em profundidade limitada
    set_expanded=set()
    def dls_rec(node, problem, depth):
        state, action, stepcost = node
        if state not in set_expanded:
            set_expanded.add(state)
            if problem.isGoalState(state):
                return action
            elif depth == 0:
                return 'cut'
            else:
                cut = False
                for successor, action_x, cost in problem.getSuccessors(state):
                    node_child = (successor, action+[action_x], cost)
                    result = dls_rec(node_child, problem, depth-1)
                    if result == 'cut':
                        cut = True
                    elif result is not None:
                        return result
                return 'cut' if cut else None

    node = (problem.getStartState(), [], 0)
    return dls_rec(node, problem, depth)

def iterativeDeepeningSearch(problem):
    """
    Start with depth = 0.
    Search the deepest nodes in the search tree first up to a given depth.
    If solution not found, increment depth limit and start over.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """
    ############################################################################
    # getStartState -> Returns the start state for the search problem.
    # isGoalState -> True or false.
    # getSuccessors -> Return list of triples, (successor, action, stepCost).
    # itertools p/ loop 0 -> infinito
    ############################################################################
    import itertools
    for depth in itertools.count():
        result = dls(problem, depth)
        if result != 'cut':
            return result

    #==================================PRONTO==================================#
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    node = (problem.getStartState(), 0, [])
    border = util.PriorityQueue()
    border.push(node, 0)
    set_expanded = set()
    while True:
        if border.isEmpty():
            return False
        state, stepcost, action = border.pop()
        if problem.isGoalState(state):
            return action
        if state not in set_expanded:
            set_expanded.add(state)
            successors = problem.getSuccessors(state)
            for successor, action_x, cost in successors:
                cost_x = stepcost+cost
                node_final = (successor, cost_x, action+[action_x])
                border.push(node_final, cost_x)
                
    #==================================PRONTO==================================#
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    border = util.PriorityQueue()
    border.push((problem.getStartState(), [], 1.0), 0)
    start = problem.getStartState()
    set_expanded = []
    came_from = []
    cost_so_far = []
    while True:
        if border.isEmpty():
            return False
        state, action, cost_so_far = border.pop()
        if problem.isGoalState(state):
            return action
        if state not in set_expanded:
            set_expanded.append(state)
            for successor, action_x, cost in problem.getSuccessors(state):
                new_cost = heuristic(successor, problem)
                border.push((successor, action+[action_x], cost+cost_so_far), cost+cost_so_far+new_cost)

    #==================================PRONTO==================================#


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch