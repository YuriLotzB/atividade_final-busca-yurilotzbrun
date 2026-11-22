from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        frontier = [initial]
        best_depth = {initial: 0}

        while frontier:
            current = frontier.pop()
            if best_depth.get(current, current.cost) < current.cost:
                continue
            if current.is_goal:
                return SearchResult(current, nodes_expanded, nodes_generated,
                                    max_frontier_size, current.cost)
            if current.cost >= self.depth_limit:
                continue
            nodes_expanded += 1

            for child in reversed(current.neighbors()):
                known = best_depth.get(child)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child] = child.cost
                nodes_generated += 1
                frontier.append(child)
            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
