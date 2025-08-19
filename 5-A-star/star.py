import heapq
from collections import defaultdict


def check_goal_reached(current_pos, target_pos):
    return current_pos == target_pos


def encode_position(position):
    return f"{position[0]}{position[1]}"


def is_valid_move(x, y, grid_size, obstacles):
    return 0 <= x < grid_size and 0 <= y < grid_size and obstacles[x][y] == 0


def manhattan_distance(current_pos, target_pos):
    x1, y1 = current_pos
    x2, y2 = target_pos
    return abs(x1 - x2) + abs(y1 - y2)


def generate_neighbors(position, grid_size, obstacles):
    row, col = position
    neighbors = []

    moves = [
        (1, 0), (0, 1), (1, 1),  # down, right, diagonal down-right
        (-1, 0), (-1, 1), (-1, -1),  # up, diagonal up-right, diagonal up-left
        (0, -1), (1, -1)  # left, diagonal down-left
    ]

    for dx, dy in moves:
        new_x, new_y = row + dx, col + dy
        if is_valid_move(new_x, new_y, grid_size, obstacles):
            neighbors.append([new_x, new_y])

    return neighbors


def reconstruct_path(parent_map, goal_key, position_map, grid_size, obstacles, start_pos, goal_pos):
    path = []
    current = goal_key

    while current != "START":
        path.append(position_map[current])
        current = parent_map[current]

    path.reverse()

    # Create visualization grid
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    # Mark obstacles
    for i in range(grid_size):
        for j in range(grid_size):
            if obstacles[i][j] == 1:
                grid[i][j] = "#"

    # Mark start and goal
    grid[start_pos[0]][start_pos[1]] = "i"
    grid[goal_pos[0]][goal_pos[1]] = "f"

    # Mark path
    for k in range(1, len(path)):
        x, y = path[k]
        if not (x == goal_pos[0] and y == goal_pos[1]):
            grid[x][y] = "*"

    print("\nPath Matrix:")
    for row in grid:
        print(" ".join(row))

    print("\nPath found:")
    for pos in path:
        print(f"({pos[0]},{pos[1]})", end=" ")
    print()


def solve_astar(start_pos, goal_pos, grid_size, obstacles):
    # Priority queue: (f_score, g_score, position_key)
    open_set = []
    parent_map = {}
    position_map = {}
    g_costs = {}
    closed_set = set()

    start_key = encode_position(start_pos)
    position_map[start_key] = start_pos
    parent_map[start_key] = "START"
    g_costs[start_key] = 0

    f_score = manhattan_distance(start_pos, goal_pos)
    heapq.heappush(open_set, (f_score, 0.0, start_key))

    while open_set:
        current_f, current_g, current_key = heapq.heappop(open_set)
        current_position = position_map[current_key]

        if check_goal_reached(current_position, goal_pos):
            reconstruct_path(parent_map, current_key, position_map, grid_size, obstacles, start_pos, goal_pos)
            return

        if current_key in closed_set:
            continue

        closed_set.add(current_key)

        for neighbor in generate_neighbors(current_position, grid_size, obstacles):
            neighbor_key = encode_position(neighbor)

            # Calculate step cost (diagonal moves cost 1.5, straight moves cost 1.0)
            step_cost = 1.5 if (neighbor[0] != current_position[0] and neighbor[1] != current_position[1]) else 1.0
            tentative_g = g_costs[current_key] + step_cost

            heuristic = manhattan_distance(neighbor, goal_pos)
            f_score = tentative_g + heuristic

            if neighbor_key not in g_costs or tentative_g < g_costs[neighbor_key]:
                g_costs[neighbor_key] = tentative_g
                parent_map[neighbor_key] = current_key
                position_map[neighbor_key] = neighbor
                heapq.heappush(open_set, (f_score, tentative_g, neighbor_key))

    print("No path found.")


def main():
    grid_size = int(input("Enter size of matrix: "))
    obstacles = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    print("Enter coordinates of initial position (indexed from 0):")
    start_x, start_y = map(int, input().split())
    start_position = [start_x, start_y]

    print("Enter coordinates of goal position (indexed from 0):")
    goal_x, goal_y = map(int, input().split())
    goal_position = [goal_x, goal_y]

    obstacle_count = int(input("Enter size of river: "))
    print("Enter points of river:")

    for i in range(obstacle_count):
        print(f"Point {i + 1}: ", end="")
        x, y = map(int, input().split())
        obstacles[x][y] = 1

    solve_astar(start_position, goal_position, grid_size, obstacles)


if __name__ == "__main__":
    main()