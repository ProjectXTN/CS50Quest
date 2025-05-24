import heapq
from typing import List, Tuple, Optional, Dict

def astar(
    level_map: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    tile_size: int
) -> Optional[List[Tuple[int, int]]]:
    width: int = len(level_map[0])
    height: int = len(level_map)
    start_cell: Tuple[int, int] = (start[0] // tile_size, start[1] // tile_size)
    goal_cell: Tuple[int, int] = (goal[0] // tile_size, goal[1] // tile_size)
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set: List[Tuple[int, Tuple[int, int]]] = []
    heapq.heappush(open_set, (0, start_cell))
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], int] = {start_cell: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal_cell:
            path: List[Tuple[int, int]] = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx, dy in dirs:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < width and 0 <= neighbor[1] < height:
                if level_map[neighbor[1]][neighbor[0]] != 0:
                    continue
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal_cell)
                    heapq.heappush(open_set, (f, neighbor))
    return None

def find_first_free_tile(level_map: List[List[int]]) -> Tuple[int, int]:
    """
    Returns the (x, y) of the first walkable tile (tile == 0) in the map.
    """
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            if tile == 0:
                return x, y
    return 0, 0  # Fallback (should never happen if map has at least one 0)
