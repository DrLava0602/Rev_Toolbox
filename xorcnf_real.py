import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('REAL1', type=str, 
                    help='Input file (.real format)')
parser.add_argument('REAL2', type=str, 
                    help='Input file (.real format)')
args = parser.parse_args()
real_file1 = args.REAL1
real_file2 = args.REAL2
circ_name = os.path.basename(real_file1).split('.real')[0]
cnf_file = circ_name + '.cnf'
cnffile = open(cnf_file,'w')
realfile1 = open(real_file1,'r', encoding="utf8")
realfile2 = open(real_file2,'r', encoding="utf8")
content = realfile1.readlines()
content = [line.replace('\n', '') for line in content]
content = [line for line in content if not line == '']
content = [line for line in content if line[0] != '#']

garbage = []
constants = []

for info in [line for line in content if line[0] == '.'][:-2]:
    infos = [i for i in info.split(' ') if len(i) > 0]
    label = infos[0][1:]
    rest = ' '.join(infos[1:])
    print('  - {}:\t{}'.format(label, rest))

    if label == 'numvars':
      qubit = int(rest)
    elif label == 'variables':
      bit_dict = {}
      for idx, bit_name in enumerate(rest.split(' ')):
        bit_dict[bit_name] = idx
    elif label == 'constants':
       constants = rest
    elif label == 'garbage':
       garbage = rest[::-1]

gates = [line.rstrip() for line in content if line[0] != '.']
print('  - numgates:\t{}'.format(len(gates)))

print(garbage)
print(constants)
currentvar = []
for i in range(qubit):
    currentvar.append(i+1)
nextvar = qubit+1
xorclause = []
tar_andclause = []
andclause = []
output_andclause = []
regs_1= [[] for i in range(qubit)]
linevar_1 = [0 for i in range(qubit)]
linesign_1 = [1 for i in range(qubit)]
regs_2= [[] for i in range(qubit)]
linevar_2 = [0 for i in range(qubit)]
linesign_2 = [1 for i in range(qubit)]
initvar_1 = [i for i in currentvar]
initvar_2 = []
print('\nConverting...', end=' ')
for idx, g in enumerate(gates):
    g_split = g.split(' ')
    numctrl = int(g_split[0][1:]) - 1
    ctr_labels = g_split[1:-1]
    tar_label = g_split[-1]
    ctr_bits = [bit_dict[c] for c in ctr_labels]
    tar_bit = bit_dict[tar_label]
    varlist = []
    andvarlist = []
    if numctrl == 0:
        varlist.append(currentvar[tar_bit])
        varlist.append(nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        # objective
        linesign_1[tar_bit] *= -1
    elif numctrl == 1:
        # functional
        varlist.append(currentvar[ctr_bits[0]])
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        # objective
        regs_1[tar_bit].append(currentvar[ctr_bits[0]])
    elif numctrl == 2:
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        andvarlist.append(currentvar[ctr_bits[0]])
        andvarlist.append(currentvar[ctr_bits[1]])
        andclause.append(andvarlist)
        # objective
        regs_1[tar_bit].append(andvar)
    else:
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        for ctlbit in ctr_bits:
            andvarlist.append(currentvar[ctlbit])
        andclause.append(andvarlist)
        # objective
        regs_1[tar_bit].append(andvar)
for i in range(qubit):
    linevar_1[i] = nextvar
    nextvar += 1
print('circuit 1 done.')

content2 = realfile2.readlines()
content2 = [line.replace('\n', '') for line in content2]
content2 = [line for line in content2 if not line == '']
content2 = [line for line in content2 if line[0] != '#']

for info in [line for line in content2 if line[0] == '.'][:-2]:
    infos2 = [i for i in info.split(' ') if len(i) > 0]
    label2 = infos2[0][1:]
    rest2 = ' '.join(infos2[1:])
    print('  - {}:\t{}'.format(label2, rest2))

    if label2 == 'numvars':
      numbits2 = int(rest2)
    elif label2 == 'variables':
      bit_dict2 = {}
      for idx, bit_name in enumerate(rest2.split(' ')):
        bit_dict2[bit_name] = idx
    elif label == 'constants':
       assert constants == rest
    elif label == 'garbage':
       assert garbage == rest[::-1]

gates2 = [line.rstrip() for line in content2 if line[0] != '.']
print('  - numgates:\t{}'.format(len(gates2)))

currentvar = []
for i in range(qubit):
    currentvar.append(i+nextvar)
    initvar_2.append(i+nextvar)
nextvar = qubit + nextvar
i=0
print('\nConverting...', end=' ')
for idx, g in enumerate(gates2):
    g_split = g.split(' ')
    numctrl = int(g_split[0][1:]) - 1
    ctr_labels = g_split[1:-1]
    tar_label = g_split[-1]
    ctr_bits = [bit_dict[c] for c in ctr_labels]
    tar_bit = bit_dict[tar_label]
    varlist = []
    andvarlist = []
    if numctrl == 0:
        varlist.append(currentvar[tar_bit])
        varlist.append(nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        # objective
        linesign_2[tar_bit] *= -1
    elif numctrl == 1:
        # functional
        varlist.append(currentvar[ctr_bits[0]])
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        # objective
        regs_2[tar_bit].append(currentvar[ctr_bits[0]])
    elif numctrl == 2:
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        andvarlist.append(currentvar[ctr_bits[0]])
        andvarlist.append(currentvar[ctr_bits[1]])
        andclause.append(andvarlist)
        # objective
        regs_2[tar_bit].append(andvar)
    else:
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tar_bit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tar_bit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        for ctlbit in ctr_bits:
            andvarlist.append(currentvar[ctlbit])
        andclause.append(andvarlist)
        # objective
        regs_2[tar_bit].append(andvar)
    i += 1
for i in range(qubit):
    linevar_2[i] = nextvar
    nextvar += 1
print('circuit 2 done.')
# print(xorclause)
# print(tar_andclause)
# print(andclause)
# print(regs_1)
# print(regs_2)
# print(linevar_1)
# print(linevar_2)
# print(nextvar)
# print(initvar_1)
# print(initvar_2)

outputvars = []
for i in range(qubit):
    if garbage[i] == '-':
        output_andclause.append([linevar_1[i], -linevar_2[i], nextvar])
        output_andclause.append([-linevar_1[i], -nextvar])
        output_andclause.append([linevar_2[i], -nextvar])
        outputvars.append(nextvar)
        nextvar += 1
        output_andclause.append([-linevar_1[i], linevar_2[i], nextvar])
        output_andclause.append([linevar_1[i], -nextvar])
        output_andclause.append([-linevar_2[i], -nextvar])
        outputvars.append(nextvar)
        nextvar += 1

cnffile.write("c " + cnf_file+"\n")
cnffile.write("p cnf "+str(nextvar-1)+ " ")
num_clauses = len(xorclause) + 1
for i in range(qubit):
    num_clauses += 2
for i in range(qubit):
    if garbage[i] == '-':
        num_clauses += 6
    if constants[i] != '-':
        num_clauses += 2
    else:
        num_clauses += 1
for andc in andclause:
    num_clauses += len(andc) + 1
cnffile.write(str(num_clauses) + '\n')
for xorc in xorclause:
    cnffile.write("x")
    for var in xorc:
        cnffile.write(str(var)+" ")
    cnffile.write("0\n")
for i in range(len(andclause)):
    for var in andclause[i]:
        cnffile.write(str(-var)+" ")
    cnffile.write(str(tar_andclause[i])+" 0\n")
    for var in andclause[i]:
        cnffile.write(str(-tar_andclause[i]) + " " + str(var) + " 0\n")
for i in range(qubit):
    if regs_1[i] == [] and linesign_1[i] == 1:
        cnffile.write(str(-1*linevar_1[i])+" 0\n")
    else:
        cnffile.write("x")
        if linesign_1[i] == 1:
            cnffile.write("-")
        cnffile.write(str(linevar_1[i])+ " ")
        for var in regs_1[i]:
            cnffile.write(str(var) + " ")
        cnffile.write("0\n")
for i in range(qubit):
    if regs_2[i] == [] and linesign_2[i] == 1:
        cnffile.write(str(-1*linevar_2[i])+" 0\n")
    else:
        cnffile.write("x")
        if linesign_2[i] == 1:
            cnffile.write("-")
        cnffile.write(str(linevar_2[i])+ " ")
        for var in regs_2[i]:
            cnffile.write(str(var) + " ")
        cnffile.write("0\n")
for i in range(qubit):
    if constants[i] == '0':
        cnffile.write("-"+str(initvar_1[i])+" 0\n")
        cnffile.write("-"+str(initvar_2[i])+" 0\n")
    elif constants[i] == '1':
        cnffile.write(str(initvar_1[i])+" 0\n")
        cnffile.write(str(initvar_2[i])+" 0\n")
    else:
        cnffile.write("x"+str(initvar_1[i])+" "+str(-initvar_2[i])+" 0\n")

for clause in output_andclause:
    for var in clause:
        cnffile.write(str(var)+" ")
    cnffile.write("0\n")
for var in outputvars:
    cnffile.write(str(var)+" ")
cnffile.write("0\n")