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


# from dis import dis
# from re import S
# from turtle import distance
# from xxlimited import foo
# from pacman import GameState
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

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

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(self.index, action)
        newPos = successorGameState.getPacmanPosition(self.index)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        if len(newFood.asList()):
            fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
        else:
            fooddist = 0

        return successorGameState.getScore()[self.index] - fooddist

def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()[index]

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)



class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """
    repeatedPos = []
    for i in range(100):
        l = []
        for j in range(100):
            l.append(0)
        repeatedPos.append(l)

    def getAction(self, gameState):
        index = self.index # pacman index
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.

        Some functions you may need:
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legalMoves = gameState.getLegalActions(agent)
        legalNextState = [gameState.generateSuccessor(agent, action)
                          for action in legalMoves]
        """
        "*** YOUR CODE HERE ***"
        
        #minMax algorithm
        def minMax(gameState, depth, agent, alpha, beta):
            if gameState.isLose() or gameState.isWin() or depth == self.depth or gameState.getLegalActions(agent) == 0:
                score = self.myGetScore(gameState)
                # print(gameState.getNumFood())
                return (score, None)

            if agent < gameState.getNumPacman():
                #Pacman's turn
                values = []
                v = float('-inf')
                actions = gameState.getLegalActions(agent) 
                nextAgent = (agent + 1)%gameState.getNumAgents() #round robin rule to get the right agent
                if nextAgent == 0:
                    depth += 1
                for action in actions:
                    value , _ = minMax(gameState.generateSuccessor(agent, action), depth, (agent+1)%gameState.getNumAgents(), alpha, beta)
                    values.append(value)
                    #alpha pruning
                    v = max([value, v])
                    if v > beta:
                        return (v, action)
                    alpha = max([alpha, v])
                maxValue = max(values)
                bestIndices = [index for index in range(len(values)) if values[index] == maxValue]
                chosenIndex = random.choice(bestIndices)
                return (maxValue, actions[chosenIndex])
            else:
                #ghosts' turns
                values = []
                v = float('inf')
                actions = gameState.getLegalActions(agent)
                nextAgent = (agent + 1)%gameState.getNumAgents() #round robin rule to get the right agent
                if nextAgent == 0:
                    depth += 1
                for action in actions:
                    value, _ = minMax(gameState.generateSuccessor(agent, action), depth, (agent+1)%gameState.getNumAgents(), alpha, beta)
                    values.append(value)
                    #beta pruning
                    v = min([value, v])
                    if v < alpha:
                        return (v, action)
                    beta = min([beta, v])
                minValue = min(values)
                bestIndices = [index for index in range(len(values)) if values[index] == minValue]
                chosenIndex = random.choice(bestIndices)
                
                return (minValue, actions[chosenIndex])

        
        _, action = minMax(gameState, 0, self.index, float('-inf'), float('inf'))
        

        pos = gameState.getPacmanPosition(self.index)
        self.repeatedPos[pos[0]][pos[1]] += 1
        # print("GetAction:\n")
        # print(pos)
        # print(self.repeatedPos[pos[0]][pos[1]])
        return action


        # print("Number of Pacmans:", gameState.getNumPacman(), ", Number of ghosts:", gameState.getNumGhosts())

        # util.raiseNotDefined()

    def myGetScore(self, currentGameState):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        score = currentGameState.getScore()[self.index]
        Pos = currentGameState.getPacmanPosition(self.index)
        Food = currentGameState.getFood().asList()
        Ghosts = currentGameState.getGhostStates()
        loseDeduct = 0
        winAward = 0
        CapsulesPos = currentGameState.getCapsules()
        CapsulePenality = 0
        if(len(CapsulesPos) > 1):
            CapsulePenality = 20*util.manhattanDistance(CapsulesPos[0], Pos)
        elif len(CapsulesPos) == 1:
            distance = util.manhattanDistance(CapsulesPos[0], Pos)
            if distance > 3*self.depth:
                CapsulePenality = 20
            else: 
                CapsulePenality = (20/(3*self.depth))*distance

        score -= CapsulePenality

        #repeated states penality
        # print("GetScore\n")
        # print(Pos)
        # print(self.repeatedPos[Pos[0]][Pos[1]])
        score -= 10*self.repeatedPos[Pos[0]][Pos[1]]

        WallsCount = currentGameState.getWalls().count()

        wallPenality = 5*WallsCount

        score -= wallPenality
        # for CapsulesPo in CapsulesPos:
        #     distance = util.manhattanDistance(CapsulesPo, Pos)
        #     if CapsulePenality < distance:
        #         CapsulePenality = distance

        if currentGameState.isLose():
            loseDeduct = float('inf')
            score -= loseDeduct

        if currentGameState.isWin():
            winAward = float('inf')
            score += winAward
        
        
        foodDistances = []
        for food in Food:
            distance = util.manhattanDistance(food, Pos)
            foodDistances.append(distance)
        nearestFood = 0
        lengthFood = len(foodDistances)
        score -= 100*lengthFood
        if lengthFood < 5:
            if len(foodDistances) > 0:
                nearestFood = foodDistances[0]
        else:
            nearestFood = min(foodDistances)
        # print(lengthFood)
        score -= 10*nearestFood
        # if lengthFood <= 3 and lengthFood != 0:
        #     nearestFood *= 20
        
        #deduct expect value based on the distance from ghosts
        if currentGameState.getNumGhosts() != 0:
            GhostPoPenality = 0
            ghostDistances = []
            for Ghost in Ghosts:
                distance = util.manhattanDistance(Pos, Ghost.configuration.getPosition())
                ghostDistances.append(distance)
            nearestGhost = min(ghostDistances)
            if nearestGhost < 2:
                GhostPoPenality = 5000
            else: 
                GhostPoPenality = 100.0/nearestGhost
            score -= GhostPoPenality

        return score
    

        
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




