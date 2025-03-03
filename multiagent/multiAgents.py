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
        legalMoves = gameState.getLegalActions() #aici sunt colectate miscarile legale

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)#starea viitoare a jocului daca pacman face o anumita actiune
        newPos = successorGameState.getPacmanPosition()#pozitia lui pacman dupa ce a efectuat actiunea
        newFood = successorGameState.getFood()#mancarea ramasa in joc

        newGhostStates = successorGameState.getGhostStates() #starile si timpii fantomelor(colorate sau albe)
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()

        #stocam intr o lista distanta lui pacman fata de toate bucatile de mancare
        foodDistances = [util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        if foodDistances: 
          closestFoodDist = min(foodDistances) #o gasim pe cea mai apropiata
          score += 10 / closestFoodDist #cu cat mancarea e mai aproape, cu atat scorul e mai mare

        #tratam distanta lui pacman fata de fantome
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
          ghostPos = ghostState.getPosition()
          ghostDist = util.manhattanDistance(newPos, ghostPos) #distanta dintre pacman si fantome

          if scaredTime > 0: #tratam cazul in care avem fantoma alba
            score += 200 / ghostDist #pacman se apropie de ea
          elif ghostDist <= 1: #daca fantoma e colorata si pacman e aprope de ea aplicam penalizare
            score -= 1000


        remainingFood = successorGameState.getNumFood()
        score -= 10 * remainingFood #cu cat avem mai putine bucati de mancare, cu atat scorul e mai mare

        if newPos in currentGameState.getFood().asList():
          score += 100 #daca pozitia lui pacman coincide cu pozitia mancarii, crestem scorul

        return score

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
        "*** YOUR CODE HERE ***"
        #agentIndex = 0 pt Pacman si >= 1 pt fantome
        #depth = profunzimea de cautare; la fiecare miscare completa(pacman+toate fantomele) se adauga 1
        #game state = starea jocului
        def minimax(agentIndex, depth, gameState):

            if depth == self.depth or gameState.isWin() or gameState.isLose(): #daca s-a atind adancimea maxima sau suntem in starea de win/lose ne oprim
                return self.evaluationFunction(gameState) #si returnam scorul

            num_agents = gameState.getNumAgents() 

            if agentIndex == 0:  #daca agentul e pacman
                best_score = float('-inf')
                for action in gameState.getLegalActions(agentIndex): #iteram prin toate actiunile pe care le poate face pacman
                    successor = gameState.generateSuccessor(agentIndex, action)#generam starea urmatoare
                    score = minimax(1, depth, successor) #si apelam minimax pt prima fantoma pe aceeasi adancime
                    best_score = max(best_score, score) #maximizam scorul pt pacman
                return best_score

            else:  #daca agentul e fantoma reducem scorul
                best_score = float('inf')  # Change to minimizing score
                for action in gameState.getLegalActions(agentIndex): #iteram prin fiecare actiune si luam succesorul
                    successor = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == num_agents - 1:  # ultima fantoma
                        score = minimax(0, depth + 1, successor)  #agentul devinde iar 0(pacman) si crestem adancime
                    else:
                        score = minimax(agentIndex + 1, depth, successor)  #altfel trecem la urmatoarea fantoma
                    best_score = min(best_score, score)  #minimizam scorul
                return best_score


      #alegem actiunea optima pt pacman
        best_action = None #actiunea cu cel mai mare scor calculat
        best_score = float('-inf') #cel mai mare scor
        
        for action in gameState.getLegalActions(0):  
            successor = gameState.generateSuccessor(0, action) #stare in care pacman a efectuat actiunea respectiva
            score = minimax(1, 0, successor) #calculam scorul pe care pacman il are daca efectueaza actiunea respectiva
            if score > best_score:
                best_score = score
                best_action = action #=> alegem astfel actiunea cea mai buna de realizat pentru pacman si o retunam 

        return best_action 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    #minimax cu taiere alpha-beta pt. a decide cea mai buna actiune
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf') #cea mai mare valoare minima pe care agentul o aceepta
        beta = float('inf') #cea mai mica valoare maxima pt fantome
        best_action = None
        best_score = float('-inf')

        for action in gameState.getLegalActions(0): #iteram prin toate actiunile posibile lui pacman
          #calculam scorul pentru fiecare actiune posibila
          #apelam functia min pe noua stare a jocului, 1-fantoma, 0- adancimea curenta si alpha/beta pt taiere
          successor = gameState.generateSuccessor(0, action)
          score = self.min_value(successor, 1, 0, alpha, beta)
          if score > best_score: #sctualizam scorul daca gasim unul mai bun
            best_score = score
            best_action = action
          alpha = max(alpha, best_score) #dupa fiecare actiune actualizam alpha cu cel mai bun scor de pana acum

        return best_action

    def max_value(self, gameState, depth, alpha, beta):

      if depth == self.depth or gameState.isWin() or gameState.isLose(): #daca am atins adancimea maxima de cautare/win/lose returnam scorul
        return self.evaluationFunction(gameState)

      v = float('-inf')
      for action in gameState.getLegalActions(0):
        successor = gameState.generateSuccessor(0, action)
        min_val = self.min_value(successor, 1, depth, alpha, beta)
        v = max(v, min_val)

        if v > beta:
          return v
        
        alpha = max(alpha, v)
      return v

    def min_value(self, gameState, agentIndex, depth, alpha, beta):

      if depth == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      v = float('inf')
      num_agents = gameState.getNumAgents()

      for action in gameState.getLegalActions(agentIndex):
        if agentIndex == num_agents - 1:
          successor = gameState.generateSuccessor(agentIndex, action)
          max_val =  self.max_value(successor, depth + 1, alpha, beta)
          v = min(v, max_val)
        else:
          successor = gameState.generateSuccessor(agentIndex, action)
          min_val = self.min_value(successor, agentIndex + 1, depth, alpha, beta)
          v = min(v, min_val)

        if v < alpha:
          return v
        
        beta = min(beta, v)

      return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        best_action = None
        best_score = float('-inf')

        for action in gameState.getLegalActions(0):
            score = self.expect_value(gameState.generateSuccessor(0, action), 1, 0)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def max_value(self, gameState, depth):
      #maximizeaza scorul pentru pacman
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        v = float('-inf')
        for action in gameState.getLegalActions(0):
            succesor = gameState.generateSuccessor(0, action)
            v = max(v, self.expect_value(succesor, 1, depth))
        return v

    def expect_value(self, gameState, agentIndex, depth):
      #fantoma e modelata ca un agent care face alegeri la intamplare
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        num_agents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        probability = 1.0 / len(actions) #probabilitatea ca fiecare actiune sa se intample
        
        v = 0.0
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action) #generam starea succesoare actiunii action
            
            if agentIndex == num_agents - 1:
                v += probability * self.max_value(successor, depth + 1) #inmultim valoarea actiunii cu probabilitatea ca se se intample
            else:
                v += probability * self.expect_value(successor, agentIndex + 1, depth)
        
        return v


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

