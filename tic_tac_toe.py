import os
import random
import time

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

def welcome(x_limit, o_limit, vs_ai):
    clear_screen()
    print("\033[95mWelcome to Disappearing Tic Tac Toe!\033[0m")
    print("Instructions:")
    print(" - Enter your move as row and column numbers separated by a space (e.g., 2 3).")
    print(f" - Only {x_limit} X's and {o_limit} O's can be on the board at once.")
    print(" - When a player exceeds their limit, their oldest mark disappears.")
    if vs_ai:
        print(" - You are playing against the computer (O).\n")
    else:
        print(" - You are playing against another player.\n")

def get_ai_move(board, difficulty):
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if difficulty == "1":  # Easy
        return random.choice(empty) if empty else (None, None)
    else:  # Hard
        # Minimax for best move
        best_score = -float('inf')
        best_move = None
        for (i, j) in empty:
            board[i][j] = "O"
            score = minimax(board, False)
            board[i][j] = " "
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move if best_move else (None, None)

def minimax(board, is_maximizing):
    winner = None
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if all(cell != " " for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def tic_tac_toe():
    mode = input("Play against (1) another player, (2) computer, or (3) watch AI vs AI? Enter 1, 2, or 3: ").strip()
    vs_ai = (mode == "2")
    ai_vs_ai = (mode == "3")
    if vs_ai or ai_vs_ai:
        difficulty = input("Choose computer difficulty: (1) Easy or (2) Hard: ").strip()
        if difficulty not in ("1", "2"):
            difficulty = "1"
    else:
        difficulty = None
    try:
        x_limit = int(input("How many X's can be on the board before the oldest disappears? (default 5): ") or 5)
        if x_limit < 1:
            x_limit = 5
    except ValueError:
        x_limit = 5
    try:
        o_limit = int(input("How many O's can be on the board before the oldest disappears? (default 5): ") or 5)
        if o_limit < 1:
            o_limit = 5
    except ValueError:
        o_limit = 5

    player1 = "AI X" if ai_vs_ai else (input("Enter name for Player X: ") or "Player X")
    player2 = "AI O" if ai_vs_ai else ("Computer" if vs_ai else (input("Enter name for Player O: ") or "Player O"))
    players = {"X": player1, "O": player2}

    while True:
        board = [[" " for _ in range(3)] for _ in range(3)]
        ages = [[0 for _ in range(3)] for _ in range(3)]  # track move order
        owners = [["" for _ in range(3)] for _ in range(3)]  # track who placed each move
        move_counter = 1  # unique age for each move
        current_player = "X"
        clear_screen()
        welcome(x_limit, o_limit, vs_ai or ai_vs_ai)
        print(f"{players['X']} (X) vs {players['O']} (O)\n")
        while True:
            print_board(board)
            if (vs_ai and current_player == "O") or ai_vs_ai:
                # Computer's turn (for both X and O in AI vs AI)
                if ai_vs_ai and difficulty == "2":
                    # Both AIs use minimax in hard mode
                    if current_player == "X":
                        # X tries to maximize its win (invert minimax for X)
                        def get_x_move(board):
                            empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
                            best_score = -float('inf')
                            best_move = None
                            for (i, j) in empty:
                                board[i][j] = "X"
                                score = minimax_x(board, False)
                                board[i][j] = " "
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j)
                            return best_move if best_move else (None, None)
                        def minimax_x(board, is_maximizing):
                            if check_winner(board, "X"):
                                return 1
                            if check_winner(board, "O"):
                                return -1
                            if all(cell != " " for row in board for cell in row):
                                return 0
                            if is_maximizing:
                                best_score = -float('inf')
                                for i in range(3):
                                    for j in range(3):
                                        if board[i][j] == " ":
                                            board[i][j] = "X"
                                            score = minimax_x(board, False)
                                            board[i][j] = " "
                                            best_score = max(score, best_score)
                                return best_score
                            else:
                                best_score = float('inf')
                                for i in range(3):
                                    for j in range(3):
                                        if board[i][j] == " ":
                                            board[i][j] = "O"
                                            score = minimax_x(board, True)
                                            board[i][j] = " "
                                            best_score = min(score, best_score)
                                return best_score
                        row, col = get_x_move(board)
                    else:
                        row, col = get_ai_move(board, difficulty)
                else:
                    row, col = get_ai_move(board, difficulty)
                print(f"{players[current_player]} ({current_player}) moves at {row+1} {col+1}")
                time.sleep(1.2)  # Slow down AI turns for visibility
            else:
                try:
                    move = input(f"{players[current_player]} ({current_player}), enter your move (row col): ")
                    row, col = map(int, move.strip().split())
                    row -= 1
                    col -= 1
                except (ValueError, IndexError):
                    print("Invalid input. Please enter row and column numbers between 1 and 3.")
                    continue
            if not (0 <= row < 3 and 0 <= col < 3):
                print("Row and column must be between 1 and 3.")
                continue
            if board[row][col] != " ":
                print("Cell already taken. Try again.")
                continue
            board[row][col] = current_player
            ages[row][col] = move_counter
            owners[row][col] = current_player
            move_counter += 1

            # Remove oldest if player exceeds their limit
            player_limit = x_limit if current_player == "X" else o_limit
            player_cells = [
                (ages[i][j], i, j)
                for i in range(3) for j in range(3)
                if board[i][j] == current_player
            ]
            if len(player_cells) > player_limit:
                oldest = min(player_cells)
                _, i, j = oldest
                board[i][j] = " "
                ages[i][j] = 0
                owners[i][j] = ""

            clear_screen()
            welcome(x_limit, o_limit, vs_ai or ai_vs_ai)
            print(f"{players['X']} (X) vs {players['O']} (O)\n")
            if check_winner(board, current_player):
                print_board(board)
                print(f"\033[92mCongratulations, {players[current_player]} ({current_player}) wins!\033[0m")
                break

            current_player = "O" if current_player == "X" else "X"

        replay = input("Play again? (y/n): ").strip().lower()
        if replay != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    tic_tac_toe()