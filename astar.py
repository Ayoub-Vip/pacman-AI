from pacman_module.game import Agent, Directions
from pacman_module.util import Stack, PriorityQueue


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
        
    ) + tuple(state.getCapsules()) 
    + tuple([(x,y) for x in state.getFood()[0] for y in state.getFood()[1] if state.getFood()[x][y]])



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
            return state.getNumFood()

        def g_function(state):
            # return 1.00/state.getScore()
            return 1.00/state.getScore() if state.getScore() != 0 else 0


        path = []
        fringe = PriorityQueue()
        fringe.push((state, path), heuristic_function(state))
        closed = set()

        while True:
            if fringe.isEmpty():
                return []

            priority, (current, path) = fringe.pop()
            #print(priority, path)

            if current.isWin():
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            for successor, action in current.generatePacmanSuccessors():
                fringe.push((successor, path + [action]), g_function(successor) + heuristic_function(successor))

        return path
