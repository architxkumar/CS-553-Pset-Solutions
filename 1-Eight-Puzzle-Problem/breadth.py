import copy
import time


def get_user_input():
    initial_state = []
    print("Enter the numbers between 1 and 8, 0 for blank")
    for i in range(3):
        row_input = []
        for j in range(3):
            row_input.append(int(input(f'Enter the number at {i}, {j}: ')))
        initial_state.append(row_input)
    return initial_state


class Open:
    index = -1
    queue = []

    def __init__(self, initial_state):
        Open.queue.append(initial_state)
        Open.index += 1

    @staticmethod
    def dequeue():
        if Open.index == -1:
            raise IndexError('Stack is empty')
        element = Open.queue.pop(0)
        Open.index -= 1
        return element

    @staticmethod
    def push(new_state):
        Open.index += 1
        Open.queue.append(new_state)


def generate_node(matrix):
    outputs = []
    start_boundary = 0
    end_boundary = len(matrix) - 1
    x, y = get_blank_space_cords(matrix)
    if x < 0 or y < 0:
        raise IndexError('Invalid space')

    if x - 1 >= start_boundary: outputs.append(swap_cords(matrix, x, y, x - 1, y))  # upper shift
    if x + 1 <= end_boundary: outputs.append(swap_cords(matrix, x, y, x + 1, y))  # bottom shift
    if y - 1 >= start_boundary: outputs.append(swap_cords(matrix, x, y, x, y - 1))  # left shift
    if y + 1 <= end_boundary: outputs.append(swap_cords(matrix, x, y, x, y + 1))  # right shift
    return outputs


def get_blank_space_cords(matrix):
    length = len(matrix)
    for i in range(length):
        for j in range(length):
            if matrix[i][j] == 0:
                return i, j
    return -1, -1


def swap_cords(matrix, old_x, old_y, new_x, new_y):
    new_matrix = copy.deepcopy(matrix)
    a = new_matrix[old_x][old_y]
    new_matrix[old_x][old_y] = new_matrix[new_x][new_y]
    new_matrix[new_x][new_y] = a
    return new_matrix


def main():
    initial_state = get_user_input()
    solution = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    close = []
    open_stack = Open(initial_state)
    start_time = time.time()
    explored_state = 0
    while open_stack.index != -1:
        while True:
            matrix = open_stack.dequeue()
            if matrix not in close:
                break
        explored_state += 1
        if matrix == solution:
            end_time = time.time()
            print(f'States Explored: {explored_state}')
            print(f'Solution found in {end_time - start_time} seconds')
            break
        close.append(matrix)
        generated_nodes = generate_node(matrix)
        for node in generated_nodes:
            # Check: To ensure that previously explored nodes aren't even pushed into the stack
            if node not in close:
                open_stack.push(node)


main()
