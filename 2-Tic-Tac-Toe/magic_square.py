magic_numbers = [8, 1, 6, 3, 5, 7, 4, 9, 2]


def display_board(game_board):
    print("\nBoard:")
    for row in range(3):
        print(" ", end="")
        for col in range(3):
            position = row * 3 + col
            cell = game_board[position] if game_board[position] != ' ' else str(position + 1)
            print(cell, end="")
            if col < 2:
                print(" | ", end="")
        print()
        if row < 2:
            print("---+---+---")
    print()


def has_winner(game_board, player_symbol):
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in winning_lines:
        if all(game_board[pos] == player_symbol for pos in line):
            return True
    return False


def get_player_magic_numbers(board, player_symbol):
    player_numbers = []
    for i in range(9):
        if board[i] == player_symbol:
            player_numbers.append(magic_numbers[i])
    return player_numbers


def creates_magic_fifteen(player_numbers, candidate_number):
    for i in range(len(player_numbers)):
        for j in range(i + 1, len(player_numbers)):
            if player_numbers[i] + player_numbers[j] + candidate_number == 15:
                return True
    return False


def calculate_ai_move(board):
    ai_numbers = get_player_magic_numbers(board, 'O')
    human_numbers = get_player_magic_numbers(board, 'X')

    for i in range(9):
        if board[i] == ' ' and creates_magic_fifteen(ai_numbers, magic_numbers[i]):
            return i

    for i in range(9):
        if board[i] == ' ' and creates_magic_fifteen(human_numbers, magic_numbers[i]):
            return i

    if board[4] == ' ':
        return 4

    for corner in [0, 2, 6, 8]:
        if board[corner] == ' ':
            return corner

    for edge in [1, 3, 5, 7]:
        if board[edge] == ' ':
            return edge

    for i in range(9):
        if board[i] == ' ':
            return i

    return -1


def main():
    board = [' '] * 9
    is_player_turn = True
    total_moves = 0

    print("Tic-Tac-Toe (Magic Square AI)")
    print("You are X, computer is O.")

    while True:
        display_board(board)

        if is_player_turn:
            print("User's turn")
            try:
                move = int(input("Your move (1-9): "))
                print(f"You entered: {move}")

                if move < 1 or move > 9 or board[move - 1] != ' ':
                    print("Invalid move, try again.")
                    continue

                board[move - 1] = 'X'
                total_moves += 1

                if has_winner(board, 'X'):
                    display_board(board)
                    print("You WIN!")
                    break

            except ValueError:
                print("Input error, please enter a number.")
                continue
        else:
            print("Computer's turn")
            ai_move = calculate_ai_move(board)
            print(f"Computer chooses position {ai_move + 1}")

            if ai_move == -1:
                break

            board[ai_move] = 'O'
            total_moves += 1

            if has_winner(board, 'O'):
                display_board(board)
                print("Computer WINS.")
                break

        if total_moves >= 9:
            display_board(board)
            print("It's a draw.")
            break

        is_player_turn = not is_player_turn

    print("Game over.")


if __name__ == "__main__":
    main()