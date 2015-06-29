# Open corpus files:
en_corp_file = open('C:\Python2\PA3\data_test.es', 'r')
es_corp_file = open('C:\Python2\PA3\data_test.en', 'r')

#Retrieve corpus values into lists:
enList = [] # English sentences list
en_corp_line = en_corp_file.readline()
while en_corp_line != '':
    en_corp = en_corp_line.rstrip()
    enList.append(en_corp.split(' '))
    en_corp_line = en_corp_file.readline()

en_corp_file.close()

esList = [] # Spanish sentences list
es_corp_line = es_corp_file.readline()
while es_corp_line != '':
    es_corp = es_corp_line.rstrip()
    esList.append(es_corp.split(' '))
    es_corp_line = es_corp_file.readline()

es_corp_file.close()

# Add NULL words to English list:
for line in enList:
    line.insert(0, 'NULL')


# Open files with t(f|e) and q(j | i, l, m) values:
tfile = open('C:\Python2\PA3\parameters_m2_rev.t', 'r')
qfile = open('C:\Python2\PA3\parameters_m2_rev.q', 'r')

# Extract t(f|e) parameters into dictionary:
t = {}
tline = tfile.readline()
while tline != '':
    tl = tline.rstrip()
    if not tl.split(' ')[0] in t:
        t[tl.split(' ')[0]] = {tl.split(' ')[1] : tl.split(' ')[2]}
    else:
        t[tl.split(' ')[0]].update({tl.split(' ')[1] : tl.split(' ')[2]})
    tline = tfile.readline()

# Extract q(j | i, l, m) parameters into dictionary:
q = {}
qline = qfile.readline()
while qline != '':
    ql = qline.rstrip()
    if not int(ql.split(' ')[0]) in q:
        q[int(ql.split(' ')[0])] = {(int(ql.split(' ')[1]), int(ql.split(' ')[2]), int(ql.split(' ')[3])) : ql.split(' ')[4]}
    else:
        q[int(ql.split(' ')[0])].update({(int(ql.split(' ')[1]), int(ql.split(' ')[2]), int(ql.split(' ')[3])) : ql.split(' ')[4]})
    qline = qfile.readline()


# Find arg max:
a = {} # Dictionary with alignments
for k in range(len(esList)):
    for ids, f in enumerate(esList[k]):
        i = ids + 1
        l = len(enList[k]) - 1
        m = len(esList[k])
        if not k in a:
            a[k] = [[i, max((float(q[ide][i, l, m])*float(t[e][f]), ide) for ide, e in enumerate(enList[k]))]]
        else:
            a[k].append([i, max((float(q[ide][i, l, m])*float(t[e][f]), ide) for ide, e in enumerate(enList[k]))])


'''A = {}          
for k in a:
    for item in a[k]:
        dc = {}
        if not k in A:
            dc[item[1][1]] = [item[0]]
            A[k] = dc
        else:
            if not item[1][1] in A[k]:
                dc[item[1][1]] = [item[0]]
                A[k].update(dc)
            else:
                A[k][item[1][1]].append(item[0])'''
            
# Write alignments into a file:
afile = open('C:\Python2\PA3\data_rev.p2.out', 'w')

for k in a:
    for item in a[k]:
        afile.write(str(k + 1) + ' ' + str(item[1][1]) + ' ' + str(item[0]) + '\n')
    
'''for k in A:
    for key in A[k]:
        for item in A[k][key]:
            afile.write(str(k + 1) + ' ' + str(key) + ' ' + str(item + 1) + '\n')'''

afile.close()

print 'Mission complete'


