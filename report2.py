A = [1, 2, 3, 4, 5]

def inputRelation():
    print("5x5 관계 행렬을 입력하세요! ")
    R = []
    for i in range(5):
        row = list(map(int, input().split()))
        R.append(row)
    return R

def isReflexive(R):
    for i in range(5):
        if R[i][i] != 1:
            return False
    return True

def isSymmetric(R):
    for i in range(5):
        for j in range(5):
            if R[i][j] != R[j][i]:
                return False
    return True

def isTransitive(R):
    for i in range(5):
        for j in range(5):
            if R[i][j]:
                for k in range(5):
                    if R[j][k] and not R[i][k]:
                        return False
    return True

def reflexiveClosure(R):
    newR = [row[:] for row in R]
    for i in range(5):
        newR[i][i] = 1
    return newR

def symmetricClosure(R):
    newR = [row[:] for row in R]
    for i in range(5):
        for j in range(5):
            if R[i][j] == 1:
                newR[j][i] = 1
    return newR

def transitiveClosure(R):  # Warshall algorithm
    newR = [row[:] for row in R]
    for k in range(5):
        for i in range(5):
            for j in range(5):
                if newR[i][k] and newR[k][j]:
                    newR[i][j] = 1
    return newR

def checkProperties(R):
    reflexive = isReflexive(R)
    symmetric = isSymmetric(R)
    transitive = isTransitive(R)

    print("\n")
    print(f"Reflexive : {reflexive}")
    print(f"Symmetric : {symmetric}")
    print(f"Transitive: {transitive}")

    return reflexive, symmetric, transitive

def equivalenceClosure(R):
    newR = reflexiveClosure(R)
    newR = symmetricClosure(newR)
    newR = transitiveClosure(newR)
    return newR

def relationToSet(R):
    pairs = []
    for i in range(5):
        for j in range(5):
            if R[i][j] == 1:
                pairs.append((A[i], A[j]))
    return pairs

def equivalenceClasses(R):
    classes = []
    visited = set()
    for i in range(5):
        if A[i] not in visited:
            eqClass = [A[j] for j in range(5) if R[i][j] == 1]
            for e in eqClass:
                visited.add(e)
            classes.append(eqClass)
    return classes

def equivalenceRelation(R):
    reflexive = isReflexive(R)
    symmetric = isSymmetric(R)
    transitive = isTransitive(R)
    return reflexive and symmetric and transitive

def printMatrix(R):
    for row in R:
        print(" ".join(map(str, row)))

R = inputRelation()

print("\n현재 관계 (집합의 쌍으로 표현):")
print(relationToSet(R))

reflexive, symmetric, transitive = checkProperties(R)

if equivalenceRelation(R):
    print("\n동치 관계입니다.")
    classes = equivalenceClasses(R)
    for i, cls in enumerate(classes, 1):
        print(f"Equivalence class of {cls[0]}: {cls}")
else:
    print("\n동치 관계가 아닙니다.")
    print("\n폐포 실행...")

    if not reflexive:
        print("\n반사 폐포:")
        refR = reflexiveClosure(R)
        printMatrix(refR)
    else:
        refR = R

    if not symmetric:
        print("\n대칭 폐포:")
        symR = symmetricClosure(refR)
        printMatrix(symR)
    else:
        symR = refR 

    if not transitive:
        print("\n추이 폐포:")
        transR = transitiveClosure(symR)
        printMatrix(transR)
    else:
        transR = symR

    print("\n전체 동치 폐포(equivalence closure) 생성:")
    finalR = equivalenceClosure(R)
    printMatrix(finalR)

    reflexive, symmetric, transitive = checkProperties(finalR)

    if reflexive and symmetric and transitive:
        print("\n폐포 후 동치 관계로 변환되었습니다.")
        classes = equivalenceClasses(finalR)
        for i, cls in enumerate(classes, 1):
            print(f"Equivalence class of {cls[0]}: {cls}")
    else:
        print("\n폐포 후에도 동치 관계가 아닙니다.")
