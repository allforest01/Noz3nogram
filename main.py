import game, solver
import numpy as np

if __name__ == "__main__":

    picross = game.Game()

    print()
    print("CURRENT STATE:")
    for i in range(picross.currentHeight):
        for j in range(picross.currentWidth):
            state = picross.getState(i, j)
            print(state if state else '-', end=' ')
        print()
    
    rowMeta = picross.getRowMeta()
    colMeta = picross.getColMeta()

    print()
    print("ROW META DATA:")
    for i in range(picross.currentHeight):
        for j in reversed(range(picross.longestMeta)):
            print(hex(rowMeta[i][j])[2:] if j < len(rowMeta[i]) else '-', end=' ')
        print()
    
    print()
    print("COL META DATA:")
    for j in reversed(range(picross.tallestMata)):
        for i in range(picross.currentWidth):
            print(hex(colMeta[i][j])[2:] if j < len(colMeta[i]) else '-', end=' ')
        print()
    
    for i in range(picross.currentWidth):
        rowMeta[i].reverse()

    for i in range(picross.currentWidth):
        colMeta[i].reverse()

    print()
    print("SOLVED:")
    puzz = solver.nonograms(rowMeta, colMeta)
    for i in range(picross.currentHeight):
        for j in range(picross.currentWidth):
            print('x' if puzz[i][j] == 1 else '-', end=' ')
        print()
    
    for i in range(picross.currentHeight):
        for j in range(picross.currentWidth):
            picross.setState(i, j, puzz[i][j])
