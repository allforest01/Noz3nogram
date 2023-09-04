import z3

def nonograms(rows, cols):

    s = z3.Solver()
    n = len(rows)
    m = len(cols)

    rowSegs = []
    rowSquares = [[z3.Int(f"rowSquare_{i}_{j}") for j in range(m)] for i in range(n)]
    rowMemory = dict()

    for i in range(n):
        rowSegs.append([])
        for j in range(len(rows[i])):
            rowSeg_i_j = z3.Int(f"rowSeg_{i}_{j}")
            s.add(rowSeg_i_j >= 0)
            s.add(rowSeg_i_j <= m - rows[i][j])
            # print(f"0 <= rowSeg_{i}_{j} <= {m - rows[i][j]}")
            rowSegs[i].append(rowSeg_i_j)
            x = i
            for y in range(m):
                if not (x, y) in rowMemory.keys():
                    rowMemory[(x, y)] = []
                rowMemory[(x, y)].append(z3.And(y >= rowSeg_i_j, y < rowSeg_i_j + rows[i][j]))
        for j in range(len(rows[i]) - 1):
            s.add(rowSegs[i][j] + rows[i][j] < rowSegs[i][j + 1])
    
    colSegs = []
    colSquares = [[z3.Int(f"colSquare_{i}_{j}") for j in range(m)] for i in range(n)]
    colMemory = dict()
    
    for i in range(m):
        colSegs.append([])
        for j in range(len(cols[i])):
            colSeg_i_j = z3.Int(f"colSeg_{i}_{j}")
            s.add(colSeg_i_j >= 0)
            s.add(colSeg_i_j <= n - cols[i][j])
            colSegs[i].append(colSeg_i_j)
            y = i
            for x in range(n):
                if not (x, y) in colMemory.keys():
                    colMemory[(x, y)] = []
                colMemory[(x, y)].append(z3.And(x >= colSeg_i_j, x < colSeg_i_j + cols[i][j]))
        for j in range(len(cols[i]) - 1):
            s.add(colSegs[i][j] + cols[i][j] < colSegs[i][j + 1])

    for x in range(n):
        for y in range(m):
            if (x, y) in colMemory.keys():
                s.add(z3.If(z3.Or(colMemory[(x, y)]), colSquares[x][y] == 1, colSquares[x][y] == 0))
            if (x, y) in rowMemory.keys():
                s.add(z3.If(z3.Or(rowMemory[(x, y)]), rowSquares[x][y] == 1, rowSquares[x][y] == 0))
            s.add(z3.Or(
                (rowSquares[x][y] + colSquares[x][y]) == 0,
                (rowSquares[x][y] + colSquares[x][y]) == 2))

    s.check()
    model = s.model()
    puzz = [[0 for j in range(m)] for i in range(n)]

    for x in range(n):
        for y in range(m):
            if model[rowSquares[x][y]] == 1:
                puzz[x][y] = 1
            
    return puzz
