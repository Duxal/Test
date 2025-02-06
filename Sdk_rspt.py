import random


# colocar numeros nos lugares vazios
def solve(grid):
    find = is_empty(grid)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        i = random.sample(range(1, 10), 1)[0]
        if check(grid, i, (row, col)):
            grid[row][col] = i

            if solve(grid):
                return True

            grid[row][col] = ' '

    return False


def check(grid, num, pos):
    if num in row(grid, pos[0]) or num in column(grid, pos[1]) or num in block(grid, pos):
        return False
    return True


# verificando espaços vazios
def is_empty(grid):  # pos is (i, j) -> (row, column)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ' ':
                return (i, j)
    return None



def row(grid, row):
    return grid[row]


def column(grid, col):
    return [grid[i][col] for i in range(len(grid))]


def block(grid, pos):  # pos retorno do is_empty
    box = (pos[0] // 3, pos[1] // 3)
    box_num = []
    for i in range(box[0] * 3, box[0] * 3 + 3):
        for j in range(box[1] * 3, box[1] * 3 + 3):
            box_num.append(grid[i][j])

    return box_num
