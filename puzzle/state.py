from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        # TODO: implemente a geração de estados filhos
        neighbors = []

        blank = self.blank_index
        row, col = divmod(blank, 3)

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        for dr, dc, action in moves:
            nr = row + dr
            nc = col + dc

            if 0 <= nr < 3 and 0 <= nc < 3:

                new_blank = nr * 3 + nc

                new_tiles = list(self.tiles)

                new_tiles[blank], new_tiles[new_blank] = (
                    new_tiles[new_blank],
                    new_tiles[blank],
                )

                neighbors.append(
                    State(
                        tuple(new_tiles),
                        parent=self,
                        action=action,
                        cost=self.cost + 1
                    )
                )

        return neighbors

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        # TODO: implemente a reconstrução do caminho usando self.parent
        path = []

        current = self

        while current is not None:
            path.append(current)
            current = current.parent

        path.reverse()

        return path

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        # TODO: implemente usando path()
        return [
            state.action
            for state in self.path()
            if state.action is not None
        ]
        
    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
    
    
