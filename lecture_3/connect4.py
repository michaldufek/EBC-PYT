# Function to create the game board
def create_board():
    return [['.' for _ in range(7)] for _ in range(6)]

# Function to print the game board
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()  # Print a newline for better spacing

# Function to check if a move is valid
def is_valid_location(board, col):
    return board[0][col] == '.'

# Function to drop the piece on the board
def drop_piece(board, col, piece):
    for row in reversed(board):  # Start from the bottom of the board
        if row[col] == '.':
            row[col] = piece
            break

# Function to check for win
def check_win(board, piece):
    # Check horizontal locations
    for c in range(4):
        for r in range(6):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical locations
    for c in range(7):
        for r in range(3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positively sloped diagonals
    for c in range(4):
        for r in range(3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check negatively sloped diagonals
    for c in range(4):
        for r in range(3, 6):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

# Main game loop
def play_game():
    board = create_board()
    turn = 0
    game_over = False

    while not game_over:
        # Ask the current player for their move
        print_board(board)
        col = int(input(f"Player {'1' if turn == 0 else '2'} (1-7): ")) - 1
        piece = 'X' if turn == 0 else 'O'

        if is_valid_location(board, col):
            drop_piece(board, col, piece)
            if check_win(board, piece):
                print_board(board)
                print(f"Player {'1' if turn == 0 else '2'} wins!")
                game_over = True
            turn = 1 - turn  # Switch turns between 0 and 1
        else:
            print("Invalid move, try again.")

        if all(board[0][c] != '.' for c in range(7)):  # Check if the board is full
            print_board(board)
            print("Game over, it's a draw!")
            game_over = True

# Start the game
play_game()

# EoF