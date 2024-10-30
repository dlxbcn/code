import pygame
import sys

# 初始化 Pygame
pygame.init()

# 常量定义
WINDOW_SIZE = 1000  # 窗口宽度
WINDOW_HEIGHT = 900  # 窗口高度
GRID_SIZE = 50    
GRID_COUNT = 15   
PIECE_SIZE = 40   
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# 调整按钮位置到右侧
BUTTON_X = WINDOW_SIZE - BUTTON_WIDTH - 40  # 距离右边界40像素
BUTTON_Y = 200  # 开始按钮的Y坐标
AI_BUTTON_Y = BUTTON_Y + BUTTON_HEIGHT + 20  # AI按钮在开始按钮下方

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)

# 创建窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption("五子棋")

# 棋盘数据 (0:空, 1:黑, 2:白)
board = [[0] * GRID_COUNT for _ in range(GRID_COUNT)]
current_player = 1  # 1代表黑棋，2代表白棋
game_started = False
winner = None

# AI相关变量
ai_mode = True
is_ai_turn = True

def draw_board():
    screen.fill(BROWN)
    # 画棋盘线
    board_size = GRID_SIZE * (GRID_COUNT - 1)
    start_x = (WINDOW_SIZE - board_size) // 2 - 100  # 向左偏移100像素，为右侧按钮留出空间
    start_y = (WINDOW_HEIGHT - board_size) // 2
    
    for i in range(GRID_COUNT):
        # 横线
        pygame.draw.line(screen, BLACK, 
                        (start_x, start_y + i * GRID_SIZE),
                        (start_x + board_size, start_y + i * GRID_SIZE))
        # 竖线
        pygame.draw.line(screen, BLACK,
                        (start_x + i * GRID_SIZE, start_y),
                        (start_x + i * GRID_SIZE, start_y + board_size))
    
    # 添加中心点
    center_x = start_x + board_size // 2
    center_y = start_y + board_size // 2
    pygame.draw.circle(screen, BLACK, (center_x, center_y), 8)

def draw_pieces():
    board_size = GRID_SIZE * (GRID_COUNT - 1)
    start_x = (WINDOW_SIZE - board_size) // 2 - 100  # 保持与draw_board中相同的偏移
    start_y = (WINDOW_HEIGHT - board_size) // 2
    
    for i in range(GRID_COUNT):
        for j in range(GRID_COUNT):
            if board[i][j] == 1:  # 黑棋
                pygame.draw.circle(screen, BLACK,
                                 (start_x + i * GRID_SIZE,
                                  start_y + j * GRID_SIZE),
                                 PIECE_SIZE // 2)
            elif board[i][j] == 2:  # 白棋
                pygame.draw.circle(screen, WHITE,
                                 (start_x + i * GRID_SIZE,
                                  start_y + j * GRID_SIZE),
                                 PIECE_SIZE // 2)

def check_win(x, y):
    # 检查四个方向：横向、纵向、左斜、右斜
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    
    for dx, dy in directions:
        count = 1
        # 正向检查
        tx, ty = x + dx, y + dy
        while 0 <= tx < GRID_COUNT and 0 <= ty < GRID_COUNT and board[tx][ty] == board[x][y]:
            count += 1
            tx += dx
            ty += dy
        # 反向检查
        tx, ty = x - dx, y - dy
        while 0 <= tx < GRID_COUNT and 0 <= ty < GRID_COUNT and board[tx][ty] == board[x][y]:
            count += 1
            tx -= dx
            ty -= dy
        if count >= 5:
            return True
    return False

def draw_button():
    button_color = GREEN if not game_started or winner else GRAY
    button_text = "Start" if not game_started else "ReStart"
    
    # 绘制按钮
    pygame.draw.rect(screen, button_color, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    # 绘制按钮文字
    font = pygame.font.Font(None, 36)
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH//2, BUTTON_Y + BUTTON_HEIGHT//2))
    screen.blit(text, text_rect)

def draw_winner():
    if winner:
        font = pygame.font.Font(None, 48)
        text = font.render(f"Player {'Black' if winner == 1 else 'White'} is the winner!", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_SIZE//2, 50))
        screen.blit(text, text_rect)

def reset_game():
    global board, current_player, winner, game_started, is_ai_turn
    board = [[0] * GRID_COUNT for _ in range(GRID_COUNT)]
    current_player = 1
    winner = None
    game_started = True
    is_ai_turn = False

def evaluate_position(x, y, player):
    """评估某个位置的分数"""
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    total_score = 0
    
    for dx, dy in directions:
        # 在每个方向上计算连子数和空位
        count = 1
        space_before = space_after = False
        blocked_before = blocked_after = False
        
        # 正向检查
        tx, ty = x + dx, y + dy
        while 0 <= tx < GRID_COUNT and 0 <= ty < GRID_COUNT:
            if board[tx][ty] == player:
                count += 1
            elif board[tx][ty] == 0:
                space_after = True
                break
            else:
                blocked_after = True
                break
            tx += dx
            ty += dy
            
        # 反向检查
        tx, ty = x - dx, y - dy
        while 0 <= tx < GRID_COUNT and 0 <= ty < GRID_COUNT:
            if board[tx][ty] == player:
                count += 1
            elif board[tx][ty] == 0:
                space_before = True
                break
            else:
                blocked_before = True
                break
            tx -= dx
            ty -= dy
        
        # 根据连子数和空位评分
        if count >= 5:
            total_score += 100000
        elif count == 4:
            if space_before and space_after:
                total_score += 10000  # 活四
            elif space_before or space_after:
                total_score += 1000   # 冲四
        elif count == 3:
            if space_before and space_after:
                total_score += 1000   # 活三
            elif space_before or space_after:
                total_score += 100    # 眠三
        elif count == 2:
            if space_before and space_after:
                total_score += 100    # 活二
            elif space_before or space_after:
                total_score += 10     # 眠二
    
    return total_score

def ai_move():
    """AI下棋"""
    best_score = -1
    best_move = None
    
    # 对手是人类玩家
    opponent = 1
    
    # 遍历所有空位
    for i in range(GRID_COUNT):
        for j in range(GRID_COUNT):
            if board[i][j] == 0:
                # 评估AI下在这个位置的分数
                ai_score = evaluate_position(i, j, 2)
                # 评估对手下在这个位置的分数
                opponent_score = evaluate_position(i, j, 1)
                
                # 综合评分：既要考虑进攻也要考虑防守
                total_score = ai_score + opponent_score * 0.8
                
                if total_score > best_score:
                    best_score = total_score
                    best_move = (i, j)
    
    if best_move:
        return best_move
    return None

def draw_ai_button():
    """绘制AI模式切换按钮"""
    button_color = GREEN if not ai_mode else GRAY
    button_text = "AI ON" if not ai_mode else "2 Player"
    
    pygame.draw.rect(screen, button_color, (BUTTON_X, AI_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    font = pygame.font.Font(None, 36)
    text = font.render(button_text, True, WHITE)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH//2, AI_BUTTON_Y + BUTTON_HEIGHT//2))
    screen.blit(text, text_rect)

def get_grid_position(pos):
    x, y = pos
    board_size = GRID_SIZE * (GRID_COUNT - 1)
    start_x = (WINDOW_SIZE - board_size) // 2 - 100  # 保持与draw_board中相同的偏移
    start_y = (WINDOW_HEIGHT - board_size) // 2
    
    grid_x = round((x - start_x) / GRID_SIZE)
    grid_y = round((y - start_y) / GRID_SIZE)
    
    return grid_x, grid_y

# 主游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            # 检查是否点击按钮
            if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH:
                if BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
                    reset_game()
                    continue
                elif AI_BUTTON_Y <= y <= AI_BUTTON_Y + BUTTON_HEIGHT:
                    if not game_started:
                        ai_mode = not ai_mode
                    continue
            
            # 只有游戏开始且没有获胜者且不是AI回合时才能下棋
            if game_started and not winner and not is_ai_turn:
                grid_x, grid_y = get_grid_position(event.pos)
                if 0 <= grid_x < GRID_COUNT and 0 <= grid_y < GRID_COUNT and board[grid_x][grid_y] == 0:
                    board[grid_x][grid_y] = current_player
                    
                    if check_win(grid_x, grid_y):
                        winner = current_player
                    else:
                        current_player = 3 - current_player
                        if ai_mode and current_player == 2:
                            is_ai_turn = True
    
    # AI回合
    if game_started and not winner and ai_mode and is_ai_turn:
        ai_pos = ai_move()
        if ai_pos:
            grid_x, grid_y = ai_pos
            board[grid_x][grid_y] = current_player
            if check_win(grid_x, grid_y):
                winner = current_player
            else:
                current_player = 3 - current_player
            is_ai_turn = False
    
    # 绘制游戏画面
    draw_board()
    if game_started:
        draw_pieces()
    draw_button()
    draw_ai_button()
    if winner:
        draw_winner()
    pygame.display.flip()

pygame.quit()
sys.exit()    