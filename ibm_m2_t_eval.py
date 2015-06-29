# Open corpus files:
en_corp_file = open('C:\Python2\PA3\corpus.es', 'r')
es_corp_file = open('C:\Python2\PA3\corpus.en', 'r')

#Retrieve corpus values into lists:
engList = [] # English sentences list
en_corp_line = en_corp_file.readline()
while en_corp_line != '':
    en_corp = en_corp_line.rstrip()
    engList.append(en_corp.split(' '))
    en_corp_line = en_corp_file.readline()

en_corp_file.close()

espList = [] # Spanish sentences list
es_corp_line = es_corp_file.readline()
while es_corp_line != '':
    es_corp = es_corp_line.rstrip()
    espList.append(es_corp.split(' '))
    es_corp_line = es_corp_file.readline()

es_corp_file.close()

# Delete all empty sentences:
ri = []
for k in range(len(espList)):
    if engList[k] == [''] or espList[k] == ['']:
        ri.append(k)

# Create lists without empty sentences:
enList = [i for j, i in enumerate(engList) if j not in ri]
esList = [i for j, i in enumerate(espList) if j not in ri]

# Add NULL to English sentences:
for k in range(len(esList)):
    enList[k].insert(0,'NULL')


# EM algorithm

# Initial t(f|e) parameters:
t = {}  # Dictionary to store t(f|e) parameters

tfile = open('C:\Python2\PA3\parameters_m1_rev.t', 'r')

for line in tfile:
    e = line.split(' ')[0]
    f = line.split(' ')[1]
    p = line.split(' ')[2]
    if not e in t:
        t[e] = {f : float(p)}
    else:
        t[e].update({f : float(p)})

tfile.close()

# Initial q(j | i, l, m) parameters values:
q = {} # Dictionary to store q

for k in range(len(esList)):
    l = len(enList[k])-1
    m = len(esList[k])
    for j in range(l+1):
        for i in range(1, m+1):
            if not j in q:
                q[j] = {(i, l, m) : 1/float(l+1)}
            else:
                q[j].update({(i, l, m) : 1/float(l+1)})


# Algorithm start:

a = 0
while a < 5: # To make 5 iterations

    # Count sums of t for each sentence:
    tsum = {}
    for k in range(len(esList)):
        tsum[(k, f)] = 0
        for ids, f in enumerate(esList[k]):
            for ide, e in enumerate(enList[k]):
                l = len(enList[k])-1
                m = len(esList[k])
                i = ids + 1
                tsum[(k, f)] = sum(t[e][f] * q[j][(i, l, m)] for j, e in enumerate(enList[k]))
                

    # Main iteration:
    c = {} # Dictionary to store p counts
    cq = {} # Dictionary to store q counts
    delta = {} # Dictionary to store deltas
    for k in range(len(esList)):
        for i in range(1, len(esList[k])+1):
            for j in range(len(enList[k])):
                e = enList[k][j]
                f = esList[k][i-1]
                l = len(enList[k])-1
                m = len(esList[k])
                # Evaluate delta(k, i, j):
                delta[k+1, i, j] = q[j][(i, l, m)] * t[e][f] / tsum[(k, f)]
                # Set all counts to 0
                if not (e, f) in c:
                    c[(e, f)] = 0
                if not e in c:
                    c[e] = 0
                if not (j, (i, l, m)) in cq:
                    cq[(j, (i, l, m))] = 0
                if not (i, l, m) in cq:
                    cq[(i, l, m)] = 0
                # Evaluate counts:
                c[(e, f)] = c[(e, f)] + delta[(k+1, i, j)]
                c[e] = c[e] + delta[(k+1, i, j)]
                cq[(j, (i, l, m))] = cq[(j, (i, l, m))] + delta[(k+1, i, j)]
                cq[(i, l, m)] = cq[(i, l, m)] + delta[(k+1, i, j)]

    # Set t(f|e) parameters:
    for e in t:
        for f in t[e]:
            t[e][f] = c[(e, f)] / c[e]

    # Set q(j | i, l, m) parameters:
    for j in q:
        for left in q[j]:
            q[j][left] = cq[(j, left)] / cq[left]

    a = a + 1


# Write t-counts and q-counts into files:
tfile = open('C:\Python2\PA3\parameters_m2_rev.t', 'w')

for e in t:
    for f in t[e]:
        tfile.write(str(e) + ' ' + str(f) + ' ' + str(t[e][f]) + ' \n')

tfile.close()

qfile = open('C:\Python2\PA3\parameters_m2_rev.q', 'w')

for j in q:
    for left in q[j]:
        qfile.write(str(j) + ' ' + str(left[0]) + ' ' + str(left[1]) + ' ' + str(left[2]) + ' ' + str(q[j][left]) + ' \n')

qfile.close()


print 'Mission complete'

        

