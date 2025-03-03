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
from util import Stack
from util import Queue
from util import PriorityQueue

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

    print "Start:", problem.getStartState() 
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #problem.getStartState() - ne da starea initiala a lui Pacman(pozitia)
    #problem.isGoalState(state) - returneaza True daca state este 'starea de obiectiv' => a ajuns la destinatia dorita
    #problem.getSuccessors(state) - returneaza o lista de tuple (succesor, actiune, cost) pt. fiecare stare vecina la care putem ajunge din state
    "*** YOUR CODE HERE ***"
    stack = Stack()
    visited = [] #aici tinem starile vizitete

    stack.push((problem.getStartState(), [])) #punem in stiva starea initiala + lista de actiuni(path-ul) efectuate pana in  acesa stare(care e vida)

    while not stack.isEmpty():
        state, path = stack.pop()

        if problem.isGoalState(state): #daca am ajuns la starea definita ca obiectiv
            return path #returnam drumul parcurs pana la ea

        if state not in visited: 
            visited.append(state)

            for succesor, action, _ in problem.getSuccessors(state):
                new_path = path + [action] #actualizam drumul pt. fiecare succesor
                stack.push((succesor, new_path)) #il punem in stiva

    util.raiseNotDefined()#exceptie

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    visited = []

    queue.push((problem.getStartState(), [])) #stocam in coada starea initiala

    while not queue.isEmpty():
        state, path = queue.pop()

        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.append(state)

            for succesor, action, _ in problem.getSuccessors(state):
                new_path = path + [action] #actualizam drumul pt fiecare succesor si il punem in coada
                queue.push((succesor, new_path))

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority_queue = PriorityQueue()
    visited = {} #dictionar in care pastram ca si key::value, starea impreuna cu, costul ei

    priority_queue.push((problem.getStartState(), [], 0), 0) #coada de prioritate contine starea, drumul parcurs pana la acea stare si costul

    while not priority_queue.isEmpty():
        state, path, cost = priority_queue.pop() #incepem cu starea start si exploreaza starile vecine
        #fiind coada de prioritari, la pop extrage nodul cu cel mai mic cost(prioritatea cea mai mica din coada)
        if problem.isGoalState(state):
            return path

        if state not in visited or cost < visited[state]: #daca nu se afla in dictionarul de stari vizitate sau am gasit un drum mai 'ieftin', actualizam dictionarul
            visited[state] = cost  
            #+parcurgem toti vecinii starii curente la care le actualizam costul, path-ul si ii adaugam in coada de prioritati
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                new_path = path + [action]
                priority_queue.push((successor, new_path, new_cost), new_cost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    heuristic ~ cat de aproape e o stare de obiectul dorit ~ propunere informata care ajuta algoritmii sa ia deccizii mai eficiente si mai rapide cu privire 
    la ce drumuri sa urmeze"""
    "*** YOUR CODE HERE ***"
    
    priority_queue = PriorityQueue()
    visited = [] #set de stari vizitate

    start_state = problem.getStartState() 
    priority_queue.push((start_state, [], 0), heuristic(start_state, problem)) #coada de prioritate contine starea, drumul parcurs pana la acea stare si costul
    #prioritate bazata pe costul curent + euristica
    while not priority_queue.isEmpty():
        state, path, cost = priority_queue.pop() #incepem cu starea start si exploreaza starile vecine
        #fiind coada de prioritari, la pip extrage nodul cu cel mai mic cost(prioritatea cea mai mica din coada)
        if problem.isGoalState(state):
            return path

        if state not in visited: #daca nu se afla in lista de stari vizitate 
            visited.append(state) 
            #+parcurgem toti vecinii starii curente la care le actualizam costul, path-ul si ii adaugam in coada de prioritati
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                new_path = path + [action]
                priority = new_cost + heuristic(successor, problem) #euristica folosita pt. a ghida cautarea mai eficienta, imbunatatind performanta
            
                priority_queue.push((successor, new_path, new_cost), priority)
    util.raiseNotDefined() 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
