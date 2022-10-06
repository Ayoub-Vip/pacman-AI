from pacman_module.game import Agent, Directions
from pacman_module.util import  manhattanDistance, PriorityQueue


def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class `pacman.GameState`.

    Returns:
        A hashable key tuple.
    """

    return (
        state.getPacmanPosition(),
        state.getFood()

    )#+tuple(state.getCapsules())+ tuple(state.getGhostStates())

    #+ tuple([(x,y) for x in state.getFood()[0] for y in state.getFood()[1] if state.getFood()[x][y]])



class PacmanAgent(Agent):
    """Pacman agent based on depth-first search (DFS)."""

    def __init__(self):
        super().__init__()

        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """

        if self.moves is None:
            self.moves = self.astar(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def astar(self, state):
        """Given a Pacman game state, returns a list of legal moves to solve
        the search layout.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A list of legal moves.
        """

        def heuristic_function(state, steps):
            """ give a state instance, returns the heuristic function based on 
            remaining number of food in addition to the average distances between sequence 
            of food
            
            Arguments: 
            state: a game state

            Returns: 
                heuritic function
            """
            foodlist = state.getFood().asList()
            position = state.getPacmanPosition()
            minLoc=0
            closest=[]
            farest=[]
            for i in range(len(foodlist)):
                man =manhattanDistance(position, foodlist[i])
                if i==0:
                        minLoc=man
                        farest = foodlist[i]
                        closest = foodlist[i]

                if man < minLoc:
                        minLoc = man
                        closest = foodlist[i]
                if man > minLoc:
                        farest = foodlist[i]
                # sumLoc += manhattanDistance(foodlist[i], foodlist[i+1] if i < len(foodlist)-1 else foodlist[i])
            far =0
            if len(closest)>0:
                far=manhattanDistance(closest, farest)
            return steps-state.getScore()+minLoc+far#+sumLoc -len(state.getCapsules())#state.getNumFood()+

        def stepCost(state , successor,cost):
            """ calculate new cost taking into consideration old state cost
                
                Arguments: 
                state: old state
                successor: new state
                cost: old cost

                Returns: 
                    new cost
            """
            successorPos=successor.getPacmanPosition()
            food = state.getFood()
            capsulees = state.getCapsules()
            # if food [successorPos[0]][successorPos[1]] is False:
            #     cost+=1
            # if capsulees[0]==successorPos[0] and capsulees[1]==successorPos[1]:
            #     print("capsule")
            #     cost+=1
            # if state.getNumFood()==successor.getNumFood():
            #     cost+=2


            return cost

        path = []
        fringe = PriorityQueue()
        cost =0
        fringe.push((state, path,cost), heuristic_function(state,0))
        closed = set()

        while True:
            if fringe.isEmpty():
                return []
            (priority, item) = fringe.pop()
            current = item[0]
            path = item[1]
            cost = item[2]

            if current.isWin():
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            for successor, action in current.generatePacmanSuccessors():
                newpath =path + [action]
                newcost = stepCost(state , successor,cost)

                fringe.push((successor, newpath,newcost),
                                    newcost+heuristic_function(successor,len(path)))
        return path

   