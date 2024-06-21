import numpy as np
import random
import csv

# 定義棋盤大小
ROWS = 6
COLS = 7

def create_board():
    """創建空棋盤"""
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    """在棋盤上放置棋子"""
    board[row][col] = piece

def is_valid_location(board, col):
    """檢查指定列是否可以下棋"""
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    """找到指定列的下一個空位"""
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    """輸出當前棋盤狀態到命令行"""
    print(np.flip(board, 0))  # 上下翻轉打印

def check_win(board, piece):
    """檢查是否獲勝"""
    # 檢查水平方向
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # 檢查垂直方向
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # 檢查左上到右下的對角線
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # 檢查左下到右上的對角線
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def save_training_data(board, move, result):
    """保存訓練數據到CSV文件"""
    with open('training_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        flat_board = board.flatten()
        writer.writerow(np.append(flat_board, [move, result]))

# 初始化CSV文件，寫入標題行
with open('training_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    headers = ['cell_' + str(i) for i in range(ROWS*COLS)] + ['move', 'result']
    writer.writerow(headers)

# 遊戲主循環，重複10000次
for game in range(10000):
    board = create_board()
    game_over = False
    turn = random.randint(0, 1)  # 隨機決定先手玩家，0為玩家1先手，1為玩家2先手
    move_counter = 0

    while not game_over and move_counter < ROWS * COLS:
        col = random.randint(0, COLS-1)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, turn + 1)

            if check_win(board, turn + 1):
                print(f"Game {game + 1}: Player {turn + 1} wins!!")
                game_over = True
                save_training_data(board, col, turn + 1)
            else:
                save_training_data(board, col, 0)

            move_counter += 1
            turn += 1
            turn %= 2

    if not game_over:
        print(f"Game {game + 1}: Draw")
        save_training_data(board, -1, 0)
