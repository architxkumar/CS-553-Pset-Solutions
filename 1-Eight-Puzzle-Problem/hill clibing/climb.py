import time
import copy
from typing import List, Tuple

Board = List[List[int]]


def calculate_heuristic(current_board: Board, goal_board: Board) -> int:
    misplaced_tiles_count = 0
    for i in range(len(current_board)):
        for j in range(len(current_board[i])):
            if current_board[i][j] != goal_board[i][j] and current_board[i][j] != 0:
                misplaced_tiles_count += 1
    return misplaced_tiles_count


def find_empty_tile_position(board: Board) -> Tuple[int, int]:
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return (i, j)
    return (-1, -1)


def are_boards_equal(board_a: Board, board_b: Board) -> bool:
    return board_a == board_b


def move_up(board: Board) -> Board:
    new_board = copy.deepcopy(board)
    row, col = find_empty_tile_position(new_board)
    if row > 0:
        new_board[row][col], new_board[row - 1][col] = new_board[row - 1][col], new_board[row][col]
    return new_board


def move_down(board: Board) -> Board:
    new_board = copy.deepcopy(board)
    row, col = find_empty_tile_position(new_board)
    if row < len(new_board) - 1:
        new_board[row][col], new_board[row + 1][col] = new_board[row + 1][col], new_board[row][col]
    return new_board


def move_left(board: Board) -> Board:
    new_board = copy.deepcopy(board)
    row, col = find_empty_tile_position(new_board)
    if col > 0:
        new_board[row][col], new_board[row][col - 1] = new_board[row][col - 1], new_board[row][col]
    return new_board


def move_right(board: Board) -> Board:
    new_board = copy.deepcopy(board)
    row, col = find_empty_tile_position(new_board)
    if col < len(new_board[0]) - 1:
        new_board[row][col], new_board[row][col + 1] = new_board[row][col + 1], new_board[row][col]
    return new_board


def solve_puzzle(start_board: Board, goal_board: Board):
    open_list: List[Tuple[int, Board]] = []
    visited_states: List[Board] = []

    start_heuristic = calculate_heuristic(start_board, goal_board)
    open_list.append((start_heuristic, start_board))

    while open_list:
        open_list.sort(key=lambda x: x[0])

        current_node = open_list.pop(0)
        current_heuristic_value = current_node[0]
        current_state = current_node[1]

        if are_boards_equal(current_state, goal_board):
            print("Goal Found!")
            print(f"Visited states: {len(visited_states)}")
            return

        visited_states.append(current_state)

        children_states = [
            move_up(current_state),
            move_down(current_state),
            move_left(current_state),
            move_right(current_state)
        ]

        for child_state in children_states:
            if child_state == current_state:
                continue

            heuristic = calculate_heuristic(child_state, goal_board)
            new_node = (heuristic, child_state)

            is_visited = any(are_boards_equal(child_state, s) for s in visited_states)
            is_in_open_list = any(are_boards_equal(child_state, s[1]) for s in open_list)

            if not is_visited and not is_in_open_list:
                open_list.append(new_node)

        open_list.sort(key=lambda x: x[0])

        if open_list and open_list[0][0] > current_heuristic_value:
            print(f"Search stopped: Heuristic of best child is greater than parent's.")
            print(f"{open_list[0][0]} > {current_heuristic_value}")
            print(f"Visited states: {len(visited_states)}")
            return

    print("Goal Not Found.")


if __name__ == "__main__":
    start_board: Board = [
        [1, 2, 3],
        [4, 5, 6],
        [8, 7, 0]
    ]
    goal_board: Board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("Starting puzzle solver...")
    start_time = time.perf_counter()

    solve_puzzle(start_board, goal_board)

    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000

    print(f"Execution time: {duration_ms:.2f} ms")