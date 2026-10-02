from collections import namedtuple
import pickle


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


def check_put_puzzle(board: list[list[str]], one_puzzle: tuple[tuple[str, ...], ...], x: int, y: int) -> bool:
    """檢查是否放得進去"""
    width = len(one_puzzle[0])
    height = len(one_puzzle)
    # 取得高度寬度
    if height + y - 1 > 7:
        return False
    if width + x - 1 > 6:
        return False
    # 檢查是否超出邊界
    for y_item, t in enumerate(one_puzzle, y):
        for x_item, b in enumerate(t, x):
            if board[y_item][x_item] != "empty" and b != "empty":
                return False  # 重疊就return False
    return True


def put_puzzle(board: list[list[str]], one_puzzle: tuple[tuple[str, ...], ...], x: int, y: int) -> None:
    """放一個拼圖"""
    for y_item, t in enumerate(one_puzzle, y):
        for x_item, b in enumerate(t, x):
            if b != "empty":
                board[y_item][x_item] = b


def add_score_board(
    score_board_info: list[list[None, list]],
    one_puzzle: tuple[tuple[str, ...], ...],
    index: int,
    puzzle_type_num: int,
    x: int,
    y: int,
    score_board: list[list[int | str]]
) -> None:
    """把score_board覆蓋到的部分+1，並且如果能放進去，就把index,puzzle,x,y加進score_board_info"""
    for y_index in range(y + len(one_puzzle) - 1, y - 1, -1):
        for x_index, value in enumerate(one_puzzle[y_index - y], x):
            if value == "empty":
                continue
            score_board[y_index][x_index] += 1
            score_board_info[y_index][x_index].append((index, puzzle_type_num, x, y))


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

all_puzzle = tuple(map(lambda x: Puzzle(get_all_puzzle(x.all_shape), x.is_used, x.RGB), all_puzzle))
solutions = [[[[] for _ in range(7)] for _ in range(31)] for _ in range(12)]
month_date_day = [None, None, None]
week = ["一", "二", "三", "四", "五", "六", "日"]


def undo(board: list[list[str]], road: list[tuple[int, int, int, int]]) -> None:
    """回到上一步"""
    item, type_num, x, y = road.pop()
    all_puzzle[item].is_used[0] = False
    one_puzzle = all_puzzle[item].all_shape[type_num]
    for y_item, t in enumerate(one_puzzle, y):
        for x_item, b in enumerate(t, x):
            if b != "empty":
                board[y_item][x_item] = "empty"


def dfs(board: list[list[str]], road: list[tuple[int, int, int, int]]) -> None:
    if len(road) == 10:
        solutions[month_date_day[0]][month_date_day[1]][month_date_day[2]].append(tuple(map(lambda x: x[1:], sorted(road))))
        # print(f"從{month_date_day[0] + 1}月、{month_date_day[1] + 1}號、星期{week[month_date_day[2]]}，找到一個解答，可能是新解答，也可能是重複的舊解答")
        return
    score_board_info = list(map(list, ((None,) * 7,) * 8))
    for y in range(8):
        for x in range(7):
            if board[y][x] == "empty":
                score_board_info[y][x] = []
    score_board: list[list[int]] = list(map(list, ((0,) * 7,) * 8))
    for row_item, row in enumerate(board):
        for value_item, value in enumerate(row):
            if value != "empty":
                score_board[row_item][value_item] = -1
    all_spellings: list[tuple[int, int, int, int]] = []
    for index in range(10):
        if all_puzzle[index].is_used[0]:
            continue
        puzzles = all_puzzle[index].all_shape
        for type_num, one_puzzle in enumerate(puzzles):
            for y in range(8):
                for x in range(7):
                    if not check_put_puzzle(board, one_puzzle, x, y):
                        continue
                    add_score_board(
                        score_board_info,
                        one_puzzle,
                        index,
                        type_num,
                        x,
                        y,
                        score_board,
                    )
    sorted_score: list[tuple[int, int, int]] = []
    for y, row in enumerate(score_board):
        for x, element in enumerate(row):
            if element != -1:
                sorted_score.append((element, x, y))
    if len(list(filter(lambda x: x[0] == 0, sorted_score))) > 0:
        return
    x, y = min(sorted_score, key=lambda x: x[0])[1:]
    for one_of_smally_x_y in score_board_info[y][x]:
        all_spellings.append(one_of_smally_x_y)
    for item, type_num, x, y in all_spellings:
        one_puzzle = all_puzzle[item].all_shape[type_num]
        put_puzzle(board, one_puzzle, x, y)
        all_puzzle[item].is_used[0] = True
        road.append((item, type_num, x, y))
        dfs(board, road)
        undo(board, road)


def main() -> None:
    """主程式"""
    month_table_y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    month_table_x = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
    date_table_y = [2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6]
    date_table_x = [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2]
    day_table_y = [6, 6, 6, 7, 7, 7, 6]
    day_table_x = [4, 5, 6, 4, 5, 6, 3]
    for month in range(12):
        for date in range(31):
            print(f"來跑{month + 1}月{date + 1}號...")
            for day in range(7):
                board = [["empty" for _ in range(7)] for _ in range(8)]
                # 處理被遮住的區塊
                board[0][6] = "cannot"
                board[1][6] = "cannot"
                for i in range(4):
                    board[7][i] = "cannot"
                month_date_day[:] = [month, date, day]
                board[month_table_y[month]][month_table_x[month]] = f"month：{month}"
                board[date_table_y[date]][date_table_x[date]] = f"date：{date}"
                board[day_table_y[day]][day_table_x[day]] = f"day：{day}"
                dfs(board, [])
                # for solution_num, solution in enumerate(solutions[month][date][day], 1):
                #     print(f"{month + 1}月、{date + 1}號、星期{week[day]}，的第{solution_num}個解答是{solution}")
            print(f"跑完了{month + 1}月{date + 1}號的一個禮拜!!!!")
    with open("12_month_all.pkl", "wb") as file:
        pickle.dump(solutions, file)


main()
