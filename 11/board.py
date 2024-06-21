import pygame
import sys
import numpy as np
import random
import time
from tensorflow.keras.models import load_model

# 定義棋盤大小
ROWS = 6
COLS = 7
SQUARESIZE = 100  # 每個格子的大小
RADIUS = int(SQUARESIZE / 2 - 5)

# 顏色定義
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 初始化 Pygame
pygame.init()

# 設置視窗大小
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
size = (width, height)

# 創建視窗
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 AI vs Player")
myfont = pygame.font.SysFont("monospace", 75)

# 載入訓練好的模型
model = load_model('connect4_model_final.h5')

def create_board():
    """創建空棋盤"""
    board = np.zeros((ROWS, COLS), dtype=int)
    return board

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

def draw_board(board):
    """在視窗上繪製棋盤和棋子"""
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def check_win(board, piece):
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

board = create_board()
print_board(board)
draw_board(board)

turn = 0  # 決定先手玩家，0為玩家1先手，1為AI先手
game_over = False

# 遊戲主循環
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # 玩家1下棋
            if turn == 0:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if check_win(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    # 玩家1下完棋，立即讓AI下棋
                    turn = 1

            print_board(board)
            draw_board(board)

            if game_over:
                pygame.time.wait(3000)

        # AI自動下棋
        if turn == 1 and not game_over:
            # AI 選擇最佳下棋位置
            time.sleep(1)  # 等待一段時間給AI計算
            prediction = model.predict(board.flatten().reshape(1, -1))  # 將當前棋盤狀態扁平化並預測
            col = np.argmax(prediction[0])  # 選擇預測概率最高的列

            while not is_valid_location(board, col):
                col = random.randint(0, COLS - 1)

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if check_win(board, 2):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            # AI下完棋，讓玩家1再次下棋
            turn = 0

            print_board(board)
            draw_board(board)

            if game_over:
                pygame.time.wait(1000)

pygame.quit()
