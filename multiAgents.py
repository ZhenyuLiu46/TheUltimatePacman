# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from util import Stack
from util import Queue

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
    to the MinimaxPacmanAgent and AlphaBetaPacmanAgent.

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
    "*** YOUR CODE HERE IF YOU WANT TO ***"
    "*** RELEVANT FOR QUESTIONS 3 AND 4***"


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal, unless the game has ended

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #print Correctaction
    #print "***************"
    return self.Searchminimax(gameState, 1, 0 )

  def Searchminimax(self, gameState, Depth, agentIndex):

    #print Correctaction
    #print "***************"
    if  gameState.isWin() or gameState.isLose() or Depth > self.depth :
        return self.evaluationFunction(gameState)


    legalActions = [action for action in gameState.getLegalActions(agentIndex) if action!='Stop']

    #print "***************"
    nextIndex = agentIndex + 1
    nextDepth = Depth
    if nextIndex >= gameState.getNumAgents():
        nextDepth += 1
        nextIndex = 0



    Evalresults = [self.Searchminimax( gameState.generateSuccessor(agentIndex, action) ,nextDepth, nextIndex) for action in legalActions]
    if agentIndex == 0 and Depth == 1:
        Correctaction = max(Evalresults)
        correctindex = [index for index in range(len(Evalresults)) if Evalresults[index] == Correctaction]
        RandomchooseIndex = random.choice(correctindex)
        return legalActions[RandomchooseIndex]

    if agentIndex == 0:
        Correctaction = max(Evalresults)

        return Correctaction
    else:
        Correctaction = min(Evalresults)

        return Correctaction





class AlphaBetaAgent(MultiAgentSearchAgent):



    def getAction(self, gameState):
      """
      Returns the minimax action using self.depth and self.evaluationFunction
      """
      "*** YOUR CODE HERE ***"
      #print v
      # print "@@@@@@@"
      bestmove = []
      agent = 0
      v = float("-inf")
      alpha = float("-inf")
      beta = float("inf")

      actions = gameState.getLegalActions(agent)
      successors = [(action, gameState.generateSuccessor(agent, action)) for action in actions]
      for successor in successors:
        prunevalue = alphabetaPrune(1, range(gameState.getNumAgents()), successor[1], self.depth, self.evaluationFunction, alpha, beta)

        if prunevalue > v:
          v = prunevalue
          bestmove = successor[0]

        if v >= beta:
          return bestmove

        alpha = max(alpha, v)
        #print v
        # print "@@@@@@@"

      return bestmove

def alphabetaPrune(agent, agentList, state, depth, evaluationFunc, alpha, beta):

      if depth <= 0 or state.isWin() == True or state.isLose() == True:
        return evaluationFunc(state)

      if agent == 0:
        v = float("-inf")
      else:
        v = float("inf")

      actions = state.getLegalActions(agent)
      for action in actions:
        successor = state.generateSuccessor(agent, action)

        if agent == 0:
          v = max(v, alphabetaPrune(agentList[agent+1], agentList, successor, depth, evaluationFunc, alpha, beta))
          alpha = max(alpha, v)
          if v >= beta:

            return v

        elif agent == agentList[-1]:
          v = min(v, alphabetaPrune(agentList[0], agentList, successor, depth - 1, evaluationFunc, alpha, beta))
          beta = min(beta, v)
          if v <= alpha:

            return v

        else:
          v = min(v, alphabetaPrune(agentList[agent+1], agentList, successor, depth, evaluationFunc, alpha, beta))
          beta = min(beta, v)
          if v <= alpha:

            return v
        # print "@@@@@@@"

      return v



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 3).

    You can store some additional information in a game-state using the
    customData dictionairy. You can store this information in the getAction
    function and retrieve it here. Note that all data will be reset
    the next time getAction is called, so if your data has to be persistent
    between calls to getAction you will have to store the data in your
    search agent and then initialize the dictionairy for every call of
    getAction.

    Also note that a deep copy of the dictionairy is created for every
    call to getSuccessor, meaning that stroring large data structures in
    the dictionairy might make you code really slow. For data that should
    be initialized once and never be altered you might want to consider
    storing in it a global variable and setting it only the first time
    getAction gets called.

    To store data in the customData dictionairy:
    currentGameState.customData['myData'] = thisIsMyData

    To get data from the customData dictionairy:
    retreivedData = currentGameState.customData['myData']

    Also, do not forget you can set some variables in the __init__ function
    of the MultiAgentSearchAgent and that your agents should still work
    on the problems provided by the autograder.
    """
    "*** YOUR CODE HERE ***"
    FoodD = []
    GhostD = []
    #ScaredD = []
    #print "here start to print"
    #print GhostD
    score = 0

    foodPos = currentGameState.getFood().asList()
    Gstates = currentGameState.getGhostStates()
    Cpos = currentGameState.getCapsules()
    ScaredGnum = 0

    currPos = list(currentGameState.getPacmanPosition())

    for ghostState in Gstates:
        if ghostState.scaredTimer is 0:
            ScaredGnum += 1
            GhostD.append(0)
            continue

        Gxy = ghostState.getPosition()
        x = abs(Gxy[0] - currPos[0])
        y = abs(Gxy[1] - currPos[1])
        if (x+y) == 0:
            GhostD.append(0)
        else:
            GhostD.append(-1.0/(x+y))

    for food in foodPos:
        x = abs(food[0] - currPos[0])
        y = abs(food[1] - currPos[1])
        FoodD.append(-1*(x+y))

    if not FoodD:
        FoodD.append(0)
    #print "here start to print"

    return max(FoodD) + min(GhostD) + currentGameState.getScore() - 100*len(Cpos) - 20*(len(Gstates) - ScaredGnum)

# Abbreviation
better = betterEvaluationFunction

class UltimateAgent(MultiAgentSearchAgent):
  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.
      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    # just initizilizing some varibles here

    global alpha
    global beta
    alpha = float("-inf")
    beta = float("inf")

    def evalFunction(state):
        newPos = state.getPacmanPosition()
        newFood = state.getFood()
        newGhostStates = state.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

          # returns the distance to the closest food (manhatten distance)
        def distClose(position, foodGrid) :
            gridInfo = foodGrid.packBits()

            value = None
            for i in range(gridInfo[0]) :
                for j in range(gridInfo[1]) :
                    if foodGrid[i][j] == True :
                        dist = ( ( abs(position[0] - i) + abs(position[1] - j) ), (i,j) )
                        if value == None :
                            value = dist
                        if dist[0] < value[0] :
                            value = dist
            if value == None :
                value = (0, position)
            return value


        score = 0

        # just addes the game score
        score= state.getScore()

        if state.isWin() :
            return 1000 + score

        # addes  1/food-count multiplied by 100 to the score if there is food left, if not returns 1000 for a win
        if newFood.count() > 0 :
            score += ( (1/newFood.count() )* 300 )

        # if the ghost isn't scared run away, if it is go get em
        for i in range(len(newGhostStates)) :
            ghostPos = newGhostStates[i].getPosition()
            if newScaredTimes[i] < 1 :
                if newPos == (ghostPos[0]-1, ghostPos[1]):
                    score = -9999
                elif newPos == (ghostPos[0]+1, ghostPos[1]):
                    score = -9999
                elif newPos == (ghostPos[0], ghostPos[1]-1):
                    score = -9999
                elif newPos == (ghostPos[0], ghostPos[1]+1):
                    score = -9999
            else :
                score += ( (1/( abs(newPos[0] - ghostPos[0]) + abs(newPos[1] - ghostPos[1])) ) * 300 )



        #subtract the distance to the closest food
        score -= distClose(newPos,newFood)[0]


        return score

    def minMax(state, checkD, agentsTurn, alpha, beta):
        agentsTurn += 1
        agentsTurn = agentsTurn % state.getNumAgents()
        if agentsTurn == 0 :
            checkD += 1
        if state.isWin() or state.isLose() or (checkD == 3) :
            return evalFunction(state)
        if agentsTurn == 0 :
            v = maxValue(state, checkD, agentsTurn, alpha, beta)
            return v
        else :
            v = minValue(state, checkD, agentsTurn, alpha, beta)
            return v

    def maxValue(state, checkD, agentsTurn, alpha, beta):
        maxVal = float("-inf")
        actions = state.getLegalActions(agentsTurn)
        if checkD == 0:
            maxVal = (maxVal, 'Stop')
            for a in actions :
                successor = state.generateSuccessor(agentsTurn,a)
                v = ( minMax(successor, checkD, agentsTurn, alpha, beta), a)
                if v[0] >= beta :
                    return v
                if v[0] > maxVal[0] :
                    maxVal = v
                alpha = max(alpha, v[0])
        else :
            for a in actions :
                successor = state.generateSuccessor(agentsTurn,a)
                v = minMax(successor, checkD, agentsTurn, alpha, beta)
                if v >= beta :
                    return v
                if v > maxVal :
                    maxVal = v
                alpha = max(alpha, v)
        #print maxVal
        return maxVal

    def minValue(state, checkD, agentsTurn, alpha, beta):
        minVal = float("inf")
        actions = state.getLegalActions(agentsTurn)
        for a in actions :
            successor = state.generateSuccessor(agentsTurn,a)
            v = minMax(successor, checkD, agentsTurn, alpha, beta)
            if v <= alpha :
                return v
            if v < minVal :
                minVal = v
            beta = min(beta, v)
        #print minVal
        return minVal

    action = minMax(gameState, -1, -1, alpha, beta)
    #print action[1]


    return action[1]
