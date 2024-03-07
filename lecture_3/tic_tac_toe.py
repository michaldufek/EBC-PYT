def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board):
    # Check horizontal, vertical, and diagonal for win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":  # Check rows
            return True
        if board[0][i] == board[1][i] == board[2][i] != " ":  # Check columns
            return True
    if board[0][0] == board[1][1] == board[2][2] != " " or board[0][2] == board[1][1] == board[2][0] != " ":  # Check diagonals
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
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid move. Please try again.")
            elif board[move // 3][move % 3] != " ":
                print("This cell is already taken. Please try again.")
            else:
                return move
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 9.")

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        move = get_player_move(board, current_player)
        board[move // 3][move % 3] = current_player

        if check_win(board):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__=="__main__":
    play_game()