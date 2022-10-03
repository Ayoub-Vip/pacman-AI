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

    def heuristic(self, state):
        """
        Given a state, returns the Manhattan distance of the nearest food.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - the Manhattan distance of the farthest food.
        """
        foodlist = state.getFood().asList()
        position = state.getPacmanPosition()
        distance = [0 for i in range(len(foodlist))]
        for i in range(len(foodlist)):
            distance[i] = manhattanDistance(position, foodlist[i])
        if distance:
            return min(distance)
        else:
            return 0
    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Return:
            A legal move as defined in `game.Directions`.
        """

        if self.moves is None:
            self.moves = self.astra(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def astra(self, state):
        """Given a Pacman game state, returns a list of legal moves to solve
        the search layout.

        Arguments:
            state: a game state. See API or class `pacman.GameState`.

        Returns:
            A list of legal moves.
        """

        path = []
        fringe = PriorityQueue()
        z = self.heuristic(state)
        fringe.push((state, path, 0), z)  # push starting state to fringe
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
                foodPresence = successor.getFood()
                if foodPresence is True:
                    newcost = newcost + 1
                else:
                    newcost = newcost + 2
                fringe.push((successor, newpath, newcost),
                                    newcost
                                    + 50 * self.heuristic(successor))
        return path
