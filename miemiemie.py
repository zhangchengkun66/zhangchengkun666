import pygame
import random
import os


# 初始化Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
# 定义更简洁的颜色常量
LIGHT_GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)
GRAY = (150, 150, 150)
BG_COLOR = (200, 200, 200)
SCORE = 0


# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goat Game")


# 加载背景图片
background_path = 'C:/Users/DEII/Desktop/照片大全/11.jpg'
try:
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except FileNotFoundError:
    print(f"背景图片文件未找到: {background_path}")
    background_image = pygame.Surface((WIDTH, HEIGHT))


# 显示游戏结束页面
def show_game_over_screen():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Your score is: {SCORE}", True, LIGHT_GRAY)
    killer_text = font.render("You are the king", True, LIGHT_GRAY)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(killer_text, (WIDTH // 2 - 100, HEIGHT // 2 + 30))
    pygame.display.flip()
    pygame.time.wait(3000)


# 显示规则说明
def show_rules():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    rules_text = font.render("Destroy your enemie!", True, DARK_GRAY)
    confirm_text = font.render("YOU WILL BE THE BEST KILLER", True, DARK_GRAY)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    screen.blit(rules_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    screen.blit(confirm_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    pygame.draw.rect(screen, DARK_GRAY, button_rect)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False


# 加载图案图片
image_paths = [
    'C:/Users/DEII/Desktop/照片大全/12.jpeg',
    'C:/Users/DEII/Desktop/照片大全/13.jpeg',
    'C:/Users/DEII/Desktop/照片大全/17.jpeg',
    'C:/Users/DEII/Desktop/照片大全/14.jpeg',
    'C:/Users/DEII/Desktop/照片大全/15.jpeg',
    'C:/Users/DEII/Desktop/照片大全/16.jpeg'
]
pattern_images = []
for path in image_paths:
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    pattern_images.append(img)


def create_game_board():
    patterns = []
    for img in pattern_images:
        for _ in range(6):
            patterns.append(img)
    random.shuffle(patterns)
    return [[patterns.pop() for _ in range(COLS)] for _ in range(ROWS)]


def draw_board(board):
    screen.blit(background_image, (0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))


def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {SCORE}", True, LIGHT_GRAY)
    if selected_difficulty:
        remaining_time = game_time - (pygame.time.get_ticks() // 1000 - start_time)
        if remaining_time < 0:
            remaining_time = 0
        time_text = font.render(f"Time: {remaining_time}s", True, LIGHT_GRAY)
        screen.blit(time_text, (WIDTH - 110, 10))
    screen.blit(score_text, (10, 10))


def check_match(board, selected):
    global SCORE
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
            SCORE += 10
            if SCORE >= 180:
                show_game_over_screen()
                return False
    return True


def handle_mouse_click(board, event, selected):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        col, row = x // TILE_SIZE, y // TILE_SIZE
        if 0 <= col < COLS and 0 <= row < ROWS:
            if board[row][col] is not None:
                if len(selected) < 2:
                    selected.append((row, col))
                if len(selected) == 2:
                    if not check_match(board, selected):
                        return
                    selected.clear()


# 显示难度选择界面
def show_difficulty_selection():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    easy_text = font.render("    easy(90s)", True, GRAY)
    normal_text = font.render("    normal(60s)", True, GRAY)
    hell_text = font.render("    hell(30s)", True, GRAY)
    back_text = font.render("返回规则", True, GRAY)
    easy_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 4 - 30, 60, 30)
    normal_rect = pygame.Rect(WIDTH // 2 - 30, HEIGHT // 2 - 30, 60, 30)
    hell_rect = pygame.Rect(WIDTH // 2 + 40, HEIGHT * 3 // 4 - 30, 60, 30)
    back_rect = pygame.Rect(10, 10, 100, 30)
    screen.blit(easy_text, (WIDTH // 2 - 70, HEIGHT // 4 - 20))
    screen.blit(normal_text, (WIDTH // 2 - 0, HEIGHT // 2 - 20))
    screen.blit(hell_text, (WIDTH // 2 + 70, HEIGHT * 3 // 4 - 20))
    screen.blit(back_text, (10, 10))
    pygame.draw.rect(screen, DARK_GRAY, easy_rect)
    pygame.draw.rect(screen, DARK_GRAY, normal_rect)
    pygame.draw.rect(screen, DARK_GRAY, hell_rect)
    pygame.draw.rect(screen, DARK_GRAY, back_rect)
    pygame.display.flip()

    selected_difficulty = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    selected_difficulty = "easy"
                    running = False
                elif normal_rect.collidepoint(event.pos):
                    selected_difficulty = "normal"
                    running = False
                elif hell_rect.collidepoint(event.pos):
                    selected_difficulty = "hell"
                    running = False
                elif back_rect.collidepoint(event.pos):
                    running = False
    return selected_difficulty


# 显示规则
show_rules()

# 显示难度选择并获取选择结果
selected_difficulty = show_difficulty_selection()
game_time = 0
if selected_difficulty == "easy":
    game_time = 90
elif selected_difficulty == "normal":
    game_time = 60
elif selected_difficulty == "hell":
    game_time = 30


# 主游戏循环
running = True
clock = pygame.time.Clock()
board = create_game_board()
selected = []
start_time = pygame.time.get_ticks() // 1000
while running:
    elapsed_time = pygame.time.get_ticks() // 1000 - start_time
    if elapsed_time >= game_time:
        show_game_over_screen()
        running = False

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_mouse_click(board, event, selected)

    screen.blit(background_image, (0, 0))
    draw_board(board)
    draw_score()
    pygame.display.flip()

pygame.quit()
