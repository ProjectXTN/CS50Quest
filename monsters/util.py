import heapq
from typing import List, Tuple, Optional, Dict

def astar(
    level_map: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    tile_size: int
) -> Optional[List[Tuple[int, int]]]:
    map_width: int = len(level_map[0])
    map_height: int = len(level_map)

    start_tile: Tuple[int, int] = (start[0] // tile_size, start[1] // tile_size)
    goal_tile: Tuple[int, int] = (goal[0] // tile_size, goal[1] // tile_size)

    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def manhattan_heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_nodes: List[Tuple[int, Tuple[int, int]]] = []
    heapq.heappush(open_nodes, (0, start_tile))

    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], int] = {start_tile: 0}

    walkable_tile_types: List[int] = [0, 2]

    while open_nodes:
        _, current_position = heapq.heappop(open_nodes)

        if current_position == goal_tile:
            path: List[Tuple[int, int]] = [current_position]
            while current_position in came_from:
                current_position = came_from[current_position]
                path.append(current_position)
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor_position: Tuple[int, int] = (
                current_position[0] + dx,
                current_position[1] + dy
            )

            if 0 <= neighbor_position[0] < map_width and 0 <= neighbor_position[1] < map_height:
                tile_value: int = level_map[neighbor_position[1]][neighbor_position[0]]

                if tile_value not in walkable_tile_types:
                    continue

                tentative_score: int = g_score[current_position] + 1
                if neighbor_position not in g_score or tentative_score < g_score[neighbor_position]:
                    came_from[neighbor_position] = current_position
                    g_score[neighbor_position] = tentative_score
                    estimated_cost: int = tentative_score + manhattan_heuristic(neighbor_position, goal_tile)
                    heapq.heappush(open_nodes, (estimated_cost, neighbor_position))

    return None

def find_first_free_tile(level_map: List[List[int]]) -> Tuple[int, int]:
    for y, row in enumerate(level_map):
        for x, tile_value in enumerate(row):
            if tile_value == 0:
                return x, y
    return (0, 0)
