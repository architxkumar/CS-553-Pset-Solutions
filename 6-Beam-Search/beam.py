def check_goal_reached(current_pos, target_pos):
    return current_pos == target_pos


def encode_position(position):
    return ''.join(str(n) for n in position)


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


def beam_search(start_pos, goal_pos, grid_size, obstacles, beam_width):
    parent_map = {}
    position_map = {}

    start_key = encode_position(start_pos)
    parent_map[start_key] = "START"
    position_map[start_key] = start_pos

    current_beam = [start_key]
    visited = set()

    while current_beam:
        candidates = []

        for key in current_beam:
            current_position = position_map[key]

            if check_goal_reached(current_position, goal_pos):
                reconstruct_path(parent_map, key, position_map, grid_size, obstacles, start_pos, goal_pos)
                return

            visited.add(key)

            for neighbor in generate_neighbors(current_position, grid_size, obstacles):
                neighbor_key = encode_position(neighbor)

                if neighbor_key in visited:
                    continue

                parent_map[neighbor_key] = key
                position_map[neighbor_key] = neighbor
                heuristic_value = manhattan_distance(neighbor, goal_pos)
                candidates.append((heuristic_value, neighbor_key))

        if not candidates:
            break

        # Sort by heuristic value and keep only top k candidates
        candidates.sort()
        current_beam = []

        for i in range(min(beam_width, len(candidates))):
            current_beam.append(candidates[i][1])

    print("No path found.")


def main():
    grid_size = int(input("Enter size of matrix: "))
    obstacles = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    print("Enter coordinates of initial position (indexed from 0): ", end="")
    start_x, start_y = map(int, input().split())
    start_position = [start_x, start_y]

    print("Enter coordinates of goal position (indexed from 0): ", end="")
    goal_x, goal_y = map(int, input().split())
    goal_position = [goal_x, goal_y]

    obstacle_count = int(input("Enter size of river: "))
    print("Enter points of river:")

    for i in range(obstacle_count):
        print(f"Point {i + 1}: ", end="")
        x, y = map(int, input().split())
        obstacles[x][y] = 1

    beam_width = int(input("Enter beam width (k): "))

    beam_search(start_position, goal_position, grid_size, obstacles, beam_width)


if __name__ == "__main__":
    main()