from Sdk_rspt import solve
from random import sample
from copy import deepcopy


def solution():
    grid = [[' ' for n in range(9)] for m in range(9)]
    solve(grid)
    return grid


# monta o jogo com base no nível de dificuldade
def maker(dificuldade='medio'):
    sol = solution()
    puzzle = deepcopy(sol)

    # Define o número de células a serem apagadas com base na dificuldade
    if dificuldade == 'facil':
        apagar_min, apagar_max = 17, 21  # Menos células apagadas
    elif dificuldade == 'medio':
        apagar_min, apagar_max = 22, 26  # Número moderado de células apagadas
    elif dificuldade == 'dificil':
        apagar_min, apagar_max = 27, 31  # Mais células apagadas
    else:
        raise ValueError("Dificuldade inválida. Escolha 'facil', 'medio' ou 'dificil'.")

    # Apaga células aleatoriamente dentro do intervalo determinado
    for i in sample(range(81), sample(range(apagar_min, apagar_max + 1), 1)[0]):
        puzzle[i // 9][i % 9] = ' '

    return puzzle, sol


# Formata o quebra-cabeça de forma amigável
def format(puzzle):
    print("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")

    for b in range(len(puzzle)):
        if b % 3 == 0 and b != 0:
            print("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣")
        if b in [1, 2, 4, 5, 7, 8]:
            print('╟───┼───┼───╫───┼───┼───╫───┼───┼───╢')
        for c in range(len(puzzle[0])):
            if c % 3 == 0:
                print("║ ", end="")
            if c in [1, 2, 4, 5, 7, 8] and c != 0:
                print('│ ', end='')
            if c == 8:
                print(str(puzzle[b][c]) + " ║")
            else:
                print(str(puzzle[b][c]) + " ", end='')

    print("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")


if __name__ == '__main__':
    dificuldade = input("Escolha a dificuldade (facil, medio, dificil): ").strip().lower()
    puzzle, sol = maker(dificuldade)
    print("\nQuebra-cabeça gerado:")
    format(puzzle)
    print("\nSolução:")
    format(sol)