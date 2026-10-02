from collections import namedtuple
import pickle
import pygame


def get_all_puzzle(
    t: tuple[tuple[bool, ...], ...],
) -> tuple[tuple[tuple[bool, ...], ...], ...]:
    """原本的一種加旋轉、翻轉七種，把重複的去掉"""
    width = len(t[0])
    height = len(t)
    ret = {t, t[::-1]}
    for _ in range(3):
        temp_t_t: tuple[tuple[str, ...], ...] = ()
        for x in range(width - 1, -1, -1):
            temp_t: tuple[str, ...] = ()
            for y in range(height):
                temp_t += (t[y][x],)
            temp_t_t += (temp_t,)
        t = temp_t_t
        ret.add(t)
        ret.add(t[::-1])
        width, height = height, width
    return tuple(sorted(tuple(ret)))


def put_puzzle(board: list[list[str]], one_puzzle: tuple[tuple[str, ...], ...], x: int, y: int) -> None:
    """放一個拼圖"""
    for y_item, t in enumerate(one_puzzle, y):
        for x_item, b in enumerate(t, x):
            if b != "empty":
                board[y_item][x_item] = b


Puzzle = namedtuple("Puzzle", ["all_shape", "is_used", "RGB"])
PuzzleInfo = namedtuple(
    "PuzzleInfo",
    [
        "red",
        "violet",
        "lime",
        "pink",
        "blue",
        "darkorange",
        "green",
        "yellow",
        "purple",
        "cyan",
    ],
)


all_puzzle = PuzzleInfo(
    Puzzle(
        (
            ("red", "red", "red", "red"),
        ),
        [False],
        (255, 0, 0),
    ),
    Puzzle(
        (
            ("violet", "violet", "violet"),
            ("empty", "violet", "empty"),
            ("empty", "violet", "empty"),
        ),
        [False],
        (238, 130, 238),
    ),
    Puzzle(
        (
            ("lime", "lime", "empty"),
            ("empty", "lime", "lime"),
        ),
        [False],
        (0, 255, 0),
    ),
    Puzzle(
        (
            ("pink", "pink", "pink"),
            ("empty", "pink", "pink"),
        ),
        [False],
        (255, 192, 203),
    ),
    Puzzle(
        (
            ("blue", "blue", "empty"),
            ("empty", "blue", "empty"),
            ("empty", "blue", "blue"),
        ),
        [False],
        (0, 0, 255),
    ),
    Puzzle(
        (
            ("empty", "darkorange", "darkorange", "darkorange"),
            ("darkorange", "darkorange", "empty", "empty"),
        ),
        [False],
        (255, 140, 0),
    ),
    Puzzle(
        (
            ("green", "green", "green"),
            ("green", "empty", "empty"),
            ("green", "empty", "empty"),
        ),
        [False],
        (0, 128, 0),
    ),
    Puzzle(
        (
            ("yellow", "yellow", "yellow"),
            ("empty", "empty", "yellow"),
        ),
        [False],
        (255, 255, 0),
    ),
    Puzzle(
        (
            ("purple", "purple", "purple"),
            ("purple", "empty", "purple"),
        ),
        [False],
        (128, 0, 128),
    ),
    Puzzle(
        (
            ("cyan", "cyan", "cyan", "cyan"),
            ("empty", "empty", "empty", "cyan"),
        ),
        [False],
        (0, 255, 255),
    ),
)

all_puzzle = PuzzleInfo(*map(lambda x: Puzzle(get_all_puzzle(x.all_shape), x.is_used, x.RGB), all_puzzle))

month_table = set(map(str, range(1, 13)))
date_table = set(map(str, range(1, 32)))
day_table = set(map(str, range(1, 8)))

month = input("輸入月份:")
while month not in month_table:
    month = input("輸入月份(只能輸入1到12):")

date = input("輸入日期:")
while date not in date_table:
    date = input("輸入日期(只能輸入1到31):")

day = input("輸入星期幾(阿拉伯數字):")
while day not in day_table:
    day = input("輸入星期幾(阿拉伯數字)(只能輸入1到7):")
print("加載中...")
with open("12_month_all.pkl", "rb") as file:
    data = pickle.load(file)
    i = data[int(month) - 1][int(date) - 1][int(day) - 1]
    print(f"一共有{len(i)}種拼法!!!!")
    type_table = set(map(str, range(1, len(i) + 1)))
    p_type = input(f"請輸入想呈現的萬年曆拼法編號(1~{len(i)}種):")
    while p_type not in type_table:
        p_type = input(f"請輸入想呈現的萬年曆拼法編號(1~{len(i)}種)(只能輸入1~{len(i)}):")
    board = [["empty" for _ in range(7)] for _ in range(8)]
    # 處理被遮住的區塊
    board[0][6] = "cannot"
    board[1][6] = "cannot"
    for j in range(4):
        board[7][j] = "cannot"
    for t, (k, x, y) in enumerate(i[int(p_type) - 1]):
        put_puzzle(board, all_puzzle[t].all_shape[k], x, y)
    print("-" * 12)
    print("-" * 12)
    for one_of in board:
        print(*one_of, sep="\t")
    print("-" * 12)
    print("-" * 12)
    print("已輸出完畢!!!!")


WIDTH, HEIGHT = 800, 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
running = True
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("幾月幾號星期幾破解器")

RED = (255, 0, 0)
VIOLET = (238, 130, 238)
LIME = (0, 255, 0)
PINK = (255, 192, 203)
BLUE = (0, 0, 255)
DARKORANGE = (255, 140, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)


font = pygame.font.SysFont("Arial", 70)
text = font.render("2026", True, (255, 255, 255))
text = pygame.transform.rotate(text, 270)
screen.blit(text, (650, 40))
font = pygame.font.SysFont("Arial", 55)
text = font.render("Puzzle - A - Day", True, (255, 255, 255))
screen.blit(text, (30, 750))


pygame.draw.line(screen, WHITE, (30, 30), (630, 30), 3)
pygame.draw.line(screen, WHITE, (30, 130), (630, 130), 3)
pygame.draw.line(screen, WHITE, (30, 230), (730, 230), 3)
pygame.draw.line(screen, WHITE, (30, 330), (730, 330), 3)
pygame.draw.line(screen, WHITE, (30, 430), (730, 430), 3)
pygame.draw.line(screen, WHITE, (30, 530), (730, 530), 3)
pygame.draw.line(screen, WHITE, (30, 630), (730, 630), 3)
pygame.draw.line(screen, WHITE, (30, 730), (730, 730), 3)
pygame.draw.line(screen, WHITE, (730, 830), (430, 830), 3)
pygame.draw.line(screen, WHITE, (30, 30), (30, 730), 3)
# 左到右
pygame.draw.line(screen, WHITE, (130, 30), (130, 730), 3)
pygame.draw.line(screen, WHITE, (230, 30), (230, 730), 3)
pygame.draw.line(screen, WHITE, (330, 30), (330, 730), 3)
pygame.draw.line(screen, WHITE, (430, 30), (430, 830), 3)
pygame.draw.line(screen, WHITE, (530, 30), (530, 830), 3)
pygame.draw.line(screen, WHITE, (630, 30), (630, 830), 3)
pygame.draw.line(screen, WHITE, (730, 230), (730, 830), 3)
# 上到下

month_str = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(month) - 1]
day_str = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"][int(day) - 1]
month_date_day_str = [month_str, date, day_str]
empty_num = 0
font = pygame.font.Font(None, 60)
# 顯示顏色
for y, one_of in enumerate(board):
    for x, one_of_one_of in enumerate(one_of):
        if one_of_one_of == "cannot":
            continue
        if one_of_one_of == "empty":
            text_surface = font.render(month_date_day_str[empty_num], True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (80 + x * 100, 80 + y * 100)
            empty_num += 1
            screen.blit(text_surface, text_rect)
            continue
        pygame.draw.rect(screen, eval(f"all_puzzle.{one_of_one_of}.RGB"), (30 + x * 100, 30 + y * 100, 100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
