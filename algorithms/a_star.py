import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

_GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = _GOAL_POS[tile]
            total += abs(row - goal_row) + abs(col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1
        counter = count()

        frontier = [(self.heuristic(initial), next(counter), initial)]
        best_g = {initial: initial.cost}
        closed = set()
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current in closed:
                continue

            if current.cost > best_g.get(current, current.cost):
                continue

            if current.is_goal:
                return SearchResult(current, nodes_expanded, nodes_generated,
                                    max_frontier_size, current.cost)
            closed.add(current)
            nodes_expanded += 1

            for child in current.neighbors():
                if child in closed:
                    continue
                if child.cost >= best_g.get(child, float("inf")):
                    continue
                best_g[child] = child.cost
                nodes_generated += 1
                f = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (f, next(counter), child))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
