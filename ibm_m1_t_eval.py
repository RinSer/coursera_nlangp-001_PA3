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


# EM algorithm

t = {}  # Dictionary to store t(f|e) parameters
pt = {} # List with possible trans words

# Initial t(f|e) parameters:
for k in range(len(esList)):
    enList[k].insert(0,'NULL')
    for e in enList[k]:
        if not e in pt:
            pt[e] = []
            for f in esList[k]:
                if not f in pt[e]:
                    pt[e].append(f)
        else:
            for f in esList[k]:
                if not f in pt[e]:
                    pt[e].append(f)
                
for k in range(len(esList)):
    for f in esList[k]:
        for e in enList[k]:
            if not e in t:
                t[e] = {f : 1/float(len(pt[e]))}
            else:
                t[e].update({f : 1/float(len(pt[e]))})


# Algorithm start:

a = 0
while a < 5: # To make 5 iterations

    # Count sums of t for each sentence:
    tsum = {}
    for k in range(len(esList)):
        tsum[(k, f)] = 0
        for f in esList[k]:
            tsum[(k, f)] = sum(t[e][f] for e in enList[k])

    # Main iteration:
    c = {} # Dictionary to store counts
    delta = {} # Dictionary to store deltas
    for k in range(len(esList)):
        for i in range(1, len(esList[k])+1):
            for j in range(len(enList[k])):
                e = enList[k][j]
                f = esList[k][i-1]
                # Evaluate delta(k, i, j):
                delta[k+1, i, j] = t[e][f] / tsum[(k, f)]
                # Set all counts to 0
                if not (e, f) in c:
                    c[(e, f)] = 0
                if not e in c:
                    c[e] = 0
                # Evaluate counts:
                c[(e, f)] = c[(e, f)] + delta[(k+1, i, j)]
                c[e] = c[e] + delta[(k+1, i, j)]

    # Set t(f|e) parameters:
    for e in t:
        for f in t[e]:
            t[e][f] = c[(e, f)] / c[e]

    a = a + 1


# Write t-counts into a file:
tfile = open('C:\Python2\PA3\parameters_m1_rev.t', 'w')

for e in t:
    for f in t[e]:
        tfile.write(str(e) + ' ' + str(f) + ' ' + str(t[e][f]) + ' \n')

tfile.close()

print 'Mission complete'

        

