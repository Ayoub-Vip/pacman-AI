from pacman_module.game import Agent, Directions
from pacman_module.util import PriorityQueue , manhattanDistance

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
    )


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

        def heuristic_function(state):
  
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
                for i in range(len(foodlist)):
                    man =manhattanDistance(position, foodlist[i])
                    if i==0:
                         minLoc=man
                    if man < minLoc:
                         minLoc = man
            
                return  minLoc+10*state.getNumFood()



        path = []
        fringe = PriorityQueue()
        cost =0
        fringe.push((state, path,cost), heuristic_function(state))
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
                
                newcost = cost
                pos=successor.getPacmanPosition()
                foodPresence = successor.getFood()
                if foodPresence[pos[0]] [pos[1]] is False:
                    newcost = newcost -1

                fringe.push((successor, newpath, newcost),
                                    newcost +heuristic_function(successor))
        return path
