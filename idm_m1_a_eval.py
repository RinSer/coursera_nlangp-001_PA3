# Open corpus files:
en_corp_file = open('C:\Python2\PA3\dev.en', 'r')
es_corp_file = open('C:\Python2\PA3\dev.es', 'r')

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


# Open file with t(f|e) values:
tfile = open('C:\Python2\PA3\parameters_m1.t', 'r')

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


# Find arg max:
a = {} # Dictionary with alignments
for k in range(len(esList)):
    for ids, f in enumerate(esList[k]):
        if not k in a:
            a[k] = [[ids, max((float(t[e][f]), enList[k].index(e)) for e in enList[k])]]
        else:
            a[k].append([ids, max((float(t[e][f]), enList[k].index(e)) for e in enList[k])])

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
afile = open('C:\Python2\PA3\dev2.p1.out', 'w')

for k in a:
    for item in a[k]:
        afile.write(str(k + 1) + ' ' + str(item[1][1]) + ' ' + str(item[0] + 1) + '\n')
    
'''for k in A:
    for key in A[k]:
        for item in A[k][key]:
            afile.write(str(k + 1) + ' ' + str(key) + ' ' + str(item + 1) + '\n')'''

afile.close()

print 'Mission complete'


