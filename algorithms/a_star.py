import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # TODO: implemente a heurística aqui
        distance = 0

        for index, value in enumerate(state.tiles):

            if value == 0:
                continue

            current_row, current_col = divmod(index, 3)
            goal_row, goal_col = divmod(value - 1, 3)

            distance += abs(current_row - goal_row)
            distance += abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        # TODO: implemente o A* aqui
        frontier = []
        heapq.heappush(frontier, (self.heuristic(initial), initial))

        visited = set()

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:

            _, current = heapq.heappop(frontier)

            if current in visited:
                continue

            visited.add(current)
            nodes_expanded += 1

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=current.cost
                )

            for neighbor in current.neighbors():

                if neighbor not in visited:

                    priority = neighbor.cost + self.heuristic(neighbor)

                    heapq.heappush(frontier, (priority, neighbor))

                    nodes_generated += 1
                    max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )