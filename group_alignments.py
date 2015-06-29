# Implement algotithm to grow alignments.


# Function to check matrix values:
def check(matx, nDict, sDict):
    matrix = matx
    for j in range(1, len(matrix)-1):
        for i in range(1, len(matrix[j])-1):
            if matrix[j][i] == 1:
                if matrix[j-1][i-1] == 0:
                    if matrix[j-1][i] == 0:
                        if matrix[j-1][i+1] == 0:
                            if matrix[j][i-1] == 0:
                                if matrix[j][i+1] == 0:
                                    if matrix[j+1][i-1] == 0:
                                        if matrix[j+1][i] == 0:
                                            if matrix[j+1][i+1] == 0:
                                                for l in [j-1, j, j+1]:
                                                    for m in [i-1, i, i+1]:
                                                        if sDict[k][m] == l:
                                                            matrix[l][m] = 1
                                                        if nDict[k][l] == m:
                                                            matrix[l][m] = 1
                                                            
    return matrix

# Open files with alignments:
esFile = open('C:\Python2\PA3\data.p2.out', 'r') # p(f|e)
enFile = open('C:\Python2\PA3\data_rev.p2.out', 'r') # p(e|f)

esDict = {} # p(f|e) dictionary
for line in esFile:
    lin = line.rstrip()
    k = int(lin.split(' ')[0])
    i = int(lin.split(' ')[2])
    j = int(lin.split(' ')[1])
    if not k in esDict:
        esDict[k] = {i : j}
    else:
        esDict[k].update({i : j})

for k in esDict:
    esDict[k].update({0 : 0})
    
esFile.close()

enDict = {} # p(e|f) dictionary
for line in enFile:
    lin = line.rstrip()
    k = int(lin.split(' ')[0])
    i = int(lin.split(' ')[1])
    j = int(lin.split(' ')[2])
    if not k in enDict:
        enDict[k] = {j : i}
    else:
        enDict[k].update({j : i})

for k in enDict:
    enDict[k].update({0 : 0})
    
enFile.close()


# Create list of Matrices for each sentence:

A = {} # Dictionary to store alignment matrices
for k in esDict:
    jm = max(j for j in enDict[k]) + 1
    im = max(i for i in esDict[k]) + 1
    matrix = [[i for i in range(im)] for j in range(jm)] # Matrix for sentence

    # Set all matrix values to zero:
    for i in matrix[0]:
        matrix[0][i] = 0
    
    for j in enDict[k]:
        for i in esDict[k]:
            matrix[j][i] = 0

    # Set to 1 matrix values for intersection of two alignments:
    for i in esDict[k]:
        j = esDict[k][i]
        if enDict[k][j] == i:
            matrix[j][i] = 1

    matrix[0][0] = 0

                                                            
    mx = check(matrix, enDict, esDict)

    matrix = check(mx, enDict, esDict)

    for j in enDict[k]:
        if all(matrix[j][i] == 0 for i in matrix[j]):
            i = enDict[k][j]
            if all(matrix[j][i] == 0 for j in range(len(matrix))):
                   matrix[j][i] = 1

    for i in esDict[k]:
        if all(matrix[j][i] == 0 for j in range(len(matrix))):
            j = esDict[k][i]
            if all(matrix[j][i] == 0 for i in matrix[j]):
                matrix[j][i] = 1
                
    
    A[k] = matrix
    

# Write grouped alignments into a file:
afile = open('C:\Python2\PA3\data_test.p3.out', 'w')

AS = {}
for k in A:
    for j in range(len(A[k])):
        for i in range(len(A[k][j])):
            if A[k][j][i] == 1 and j != 0:
                if not k in AS:
                    AS[k] = {i : j}
                else:
                    AS[k].update({i : j})

for k in AS:
    for i in AS[k]:
        j = AS[k][i]
        afile.write(str(k) + ' ' + str(j) + ' ' + str(i) + ' \n')

afile.close()

print 'Mission complete'


    

    


        
