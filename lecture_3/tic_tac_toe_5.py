def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)  # Adjusted for 5x5 grid

def check_line(line):
    return line.count(line[0]) == 5 and line[0] != " "

def check_win(board):
    # Check horizontal and vertical lines for a win
    for i in range(5):
        if check_line(board[i]):  # Check row
            return True
        if check_line([board[j][i] for j in range(5)]):  # Check column
            return True

    # Check diagonals for a win
    if check_line([board[i][i] for i in range(5)]) or check_line([board[i][4 - i] for i in range(5)]):
        return True

    return False

def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_player_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-25): ")) - 1
            if move < 0 or move > 24:
                print("Invalid move. Please try again.")
            elif board[move // 5][move % 5] != " ":
                print("This cell is already taken. Please try again.")
            else:
                return move
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 25.")

def play_game():
    board = [[" " for _ in range(5)] for _ in range(5)]
    current_player = "X"

    while True:
        print_board(board)
        move = get_player_move(board, current_player)
        board[move // 5][move % 5] = current_player

        if check_win(board):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()
