from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, max_frontier_size, initial.cost)

        frontier = deque([initial])
        visited = {initial}

        while frontier:
            current = frontier.popleft()
            nodes_expanded += 1

            for child in current.neighbors():
                if child in visited:
                    continue
                visited.add(child)
                nodes_generated += 1

                if child.is_goal:
                    return SearchResult(child, nodes_expanded, nodes_generated,
                                        max(max_frontier_size, len(frontier) + 1), child.cost)
                frontier.append(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size, 0)
