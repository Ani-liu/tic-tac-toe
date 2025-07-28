import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    print("    1   2   3")
    print("  -------------")
    for idx, row in enumerate(board):
        row_str = " | ".join([
            f"\033[91m{cell}\033[0m" if cell == "X" else f"\033[94m{cell}\033[0m" if cell == "O" else " "
            for cell in row
        ])
        print(f"{idx+1} | {row_str} |")
        print("  -------------")

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all([cell != " " for row in board for cell in row])

def welcome():
    clear_screen()
    print("\033[95mWelcome to Creative Tic Tac Toe!\033[0m")
    print("Instructions:")
    print(" - Enter your move as row and column numbers separated by a space (e.g., 2 3).")
    print(" - First player to get 3 in a row wins!\n")

def tic_tac_toe():
    welcome()
    player1 = input("Enter name for Player X: ") or "Player X"
    player2 = input("Enter name for Player O: ") or "Player O"
    players = {"X": player1, "O": player2}

    while True:
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_player = "X"
        clear_screen()
        welcome()
        print(f"{players['X']} (X) vs {players['O']} (O)\n")
        while True:
            print_board(board)
            try:
                move = input(f"{players[current_player]} ({current_player}), enter your move (row col): ")
                row, col = map(int, move.strip().split())
                row -= 1
                col -= 1
                if not (0 <= row < 3 and 0 <= col < 3):
                    print("Row and column must be between 1 and 3.")
                    continue
                if board[row][col] != " ":
                    print("Cell already taken. Try again.")
                    continue
                board[row][col] = current_player
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column numbers between 1 and 3.")
                continue

            clear_screen()
            welcome()
            print(f"{players['X']} (X) vs {players['O']} (O)\n")
            if check_winner(board, current_player):
                print_board(board)
                print(f"\033[92mCongratulations, {players[current_player]} ({current_player}) wins!\033[0m")
                break
            if is_full(board):
                print_board(board)
                print("\033[93mIt's a draw!\033[0m")
                break
            current_player = "O" if current_player == "X" else "X"

        replay = input("Play again? (y/n): ").strip().lower()
        if replay != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    tic_tac_toe()