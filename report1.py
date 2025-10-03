def inputMatrix():
    n = int(input("정방행렬의 차수를 입력하세요: "))
    matrix = []
    for i in range(n):
        row = list(map(int, input(f"{i+1}행: ").split()))
        if len(row) != n:
            raise ValueError("Row length must match n")
        matrix.append(row)
    return matrix

def printMatrix(matrix):
    for row in matrix:
        print("|",end="")
        print(" ".join(f"{val:8.4f}" for val in row),end="")
        print("  |")
    print()

def getMatrixMinor(m, i, j):
    return [row[:j]+row[j+1:] for row in (m[:i]+m[i+1:])]

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    det = 0
    for c in range(n):
        det += ((-1)**c) * matrix[0][c] * determinant(getMatrixMinor(matrix, 0, c))
    
    return det

def getTransposeMatrix(m):  
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def getAdjacentMatrix(matrix):
    n = len(matrix)
    
    if n == 1:
        return [[1]]
    
    adj = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = getMatrixMinor(matrix, i, j)
            adj[i][j] = ((-1)**(i+j)) * determinant(minor)
    return adj

def inverseByDet(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError(f"det[{matrix}] = 0 때문에 역행렬이 존재하지 않습니다.")

    adj = getAdjacentMatrix(matrix)
    transposeAdj = getTransposeMatrix(adj)
    n = len(matrix)
    inverseMat = [[transposeAdj[i][j] / det for j in range(n)] for i in range(n)]

    return inverseMat

def getGaussJordanInverse(m):
    
    n = len(m)
    # Create augmented matrix [m | I]
    aug = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(m)]
    
    for i in range(n):
                # Find pivot
        if aug[i][i] == 0:
            for k in range(i+1, n):
                if aug[k][i] != 0:
                    aug[i], aug[k] = aug[k], aug[i]
                    break
            else:
                raise ValueError(f"{m}는 Singular matrix 때문에 역행렬이 존재하지 않습니다.")
        
        # Normalize pivot row
        pivot = aug[i][i]
        aug[i] = [x / pivot for x in aug[i]]
        
        # Eliminate all other entries in column
        for j in range(n):
            if j != i:
                factor = aug[j][i]
                aug[j] = [aug[j][k] - factor * aug[i][k] for k in range(2*n)]
    
    # Extract inverse matrix
    inv = [row[n:] for row in aug]
    return inv

def multiplyMatrices(A, B):
    
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    
    if cols_A != rows_B:
        raise ValueError("Number of columns of A must equal number of rows of B")

    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

   
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):  
                result[i][j] += A[i][k] * B[k][j]

    return result

def identityMatrix(k):
    return [[1 if i == j else 0 for j in range(k)] for i in range(k)]

def checkInverse(A, B, k):
    m = multiplyMatrices(A, B)   
    n = identityMatrix(k)        
    result = equalMatrices(m, n, k)  
    
    if result:
        print("matrix multiply by its inverse is equal to identity matrix")
    else:
        print("matrix multiply by its inverse is NOT equal to identity matrix")


def equalMatrices(m1, m2, tol=1e-6):
    n = len(m1)
    for i in range(n):
        for j in range(n):
            if abs(m1[i][j] - m2[i][j]) > tol:
                return False
    return True

def main():
    matrix = inputMatrix()
    k = len(matrix)
    printMatrix(matrix)

    
    try:
        print("행렬식으로 구한 역행렬: ")
        invDet = inverseByDet(matrix)
        printMatrix(invDet)
    except ValueError as e:
        print(e)
        invDet = None
    
    try:
        print("가우스-조던 소거법으로 구한 역행렬: ")
        gaussJordanInv =  getGaussJordanInverse(matrix)
        printMatrix(gaussJordanInv)
    except ValueError as e:
        print(e)
        gaussJordanInv = None

    if invDet and gaussJordanInv:
        if equalMatrices(invDet, gaussJordanInv, k):
            print("두 방법의 결과가 동일합니다.")
        else:
            print("두 방법의 결과가 동일하지 않습니다.")

if __name__ == '__main__':
    for _ in range(3):
        main()
        print("_"*40)
    
