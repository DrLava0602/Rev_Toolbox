import os, argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('qasm', type=str, 
                    help='Input file (.qasm format)')
args = parser.parse_args()
qasm_file = args.qasm
circ_name = os.path.basename(qasm_file).split('.qasm')[0]
cnf_file = circ_name + '.cnf'

qasmfile = open(qasm_file,'r', encoding="utf8")
cnffile = open(cnf_file,'w')

content = qasmfile.readlines()
content = [line.replace('\n', '') for line in content]
str_qubit = re.findall(r'\d+', content[2])
qubit = int(str_qubit[0])
# print(qubit)
currentvar = []
for i in range(qubit):
    currentvar.append(i+1)
nextvar = qubit+1
xorclause = []
tar_andclause = []
andclause = []
regs = [[] for i in range(qubit)]
linevar = [0 for i in range(qubit)]
linesign = [1 for i in range(qubit)]
i=0
for line in content:
    if i<3:
        i = i+1
        continue
    words = line.split(' ')
    bits = re.findall(r'\d+', line)
    varlist = []
    andvarlist = []
    if words[0] == 'x':
        # functional
        tarbit = int(bits[0])
        varlist.append(currentvar[tarbit])
        varlist.append(nextvar)
        xorclause.append(varlist)
        currentvar[tarbit] = nextvar
        nextvar += 1
        # objective
        linesign[tarbit] *= -1

    elif words[0] == 'cx':
        # functional
        ctlbit = int(bits[0])
        tarbit = int(bits[1])
        varlist.append(currentvar[ctlbit])
        varlist.append(currentvar[tarbit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tarbit] = nextvar
        nextvar += 1
        # objective
        regs[tarbit].append(currentvar[ctlbit])


    elif words[0] == 'ccx':
        ctlbit1 = int(bits[0])
        ctlbit2 = int(bits[1])
        tarbit = int(bits[2])
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tarbit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tarbit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        andvarlist.append(currentvar[ctlbit1])
        andvarlist.append(currentvar[ctlbit2])
        andclause.append(andvarlist)
        # objective
        regs[tarbit].append(andvar)
    elif words[0] == 'mcx':
        tari = -1
        ctlbits = []
        for bit in bits:
            tari += 1
            ctlbits.append(int(bit))
        ctlbits.pop()
        tarbit = int(bits[tari])
        andvar = nextvar
        nextvar += 1
        varlist.append(andvar)
        varlist.append(currentvar[tarbit])
        varlist.append(-1*nextvar)
        xorclause.append(varlist)
        currentvar[tarbit] = nextvar
        nextvar += 1
        tar_andclause.append(andvar)
        for ctlbit in ctlbits:
            andvarlist.append(currentvar[ctlbit])
        andclause.append(andvarlist)
        # objective
        regs[tarbit].append(andvar)
        
    i = i+1
for i in range(qubit):
    linevar[i] = nextvar
    nextvar += 1
# print(xorclause)
# print(tar_andclause)
# print(andclause)
# print(regs)
# print(linesign)
# print(nextvar)

cnffile.write("c " + cnf_file+"\n")
cnffile.write("p cnf "+str(nextvar-1)+ " ")
num_clauses = len(xorclause) + 1
for i in range(qubit):
    if regs[i] == [] and linesign[i] == 1:
        continue
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

for var in linevar:
    cnffile.write(str(var) + " ")
cnffile.write("0\n")
for i in range(qubit):
    if regs[i] == [] and linesign[i] == 1:
        cnffile.write(str(-1*linevar[i])+" 0\n")
    else:
        cnffile.write("x")
        if linesign[i] == 1:
            cnffile.write("-")
        cnffile.write(str(linevar[i])+ " ")
        for var in regs[i]:
            cnffile.write(str(var) + " ")
        cnffile.write("0\n")



