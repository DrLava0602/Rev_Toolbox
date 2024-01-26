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
qasm_file = circ_name + '.qasm'

realfile1 = open(real_file1,'r', encoding="utf8")
realfile2 = open(real_file2,'r', encoding="utf8")
qasmfile = open(qasm_file,'w')
qasmfile.write('OPENQASM 2.0;\ninclude "qelib1.inc";\n')
# content = realfile.readlines()
# numvars = -1
# for line in content:
#     if line[0] != '#':
#         if line[0] =='.':
#             line = line[1:]
#             info = line.split()
#             if info[0] == 'numvars':
#                 numvars = int(info[1]) - int('0')
#                 varstring = 'qreg q[' + str(numvars) +']\n'
#                 qasmfile.write(varstring)
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
      numbits = int(rest)
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

qasmfile.write('qreg q['+str(numbits)+'];\n')
qasmfile.write('//'+constants+'\n')
qasmfile.write('//'+garbage+'\n')
print('\nConverting...', end=' ')
for idx, g in enumerate(gates):
    g_split = g.split(' ')
    numctrl = int(g_split[0][1:]) - 1
    ctr_labels = g_split[1:-1]
    tar_label = g_split[-1]
    ctr_bits = [bit_dict[c] for c in ctr_labels]
    tar_bit = bit_dict[tar_label]
    if numctrl == 0:
        qasmfile.write('x q['+str(tar_bit)+'];\n')
    elif numctrl == 1:
        qasmfile.write('cx q['+str(ctr_bits[0])+'], q['+str(tar_bit)+'];\n')
    elif numctrl == 2:
        qasmfile.write('ccx q['+str(ctr_bits[0])+'], q['+str(ctr_bits[1])+'], q['+str(tar_bit)+'];\n')
    else:
        mcx_str = '], q['.join(str(bits) for bits in ctr_bits)
        qasmfile.write('mcx q['+mcx_str+'], q['+str(tar_bit)+'];\n')
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

gates2 = [line.rstrip() for line in content2 if line[0] != '.']
print('  - numgates:\t{}'.format(len(gates2)))

print('\nConverting...', end=' ')
for idx, g in reversed(list(enumerate(gates2))):
    g_split2 = g.split(' ')
    numctrl2 = int(g_split2[0][1:]) - 1
    ctr_labels2 = g_split2[1:-1]
    tar_label2 = g_split2[-1]
    ctr_bits2 = [bit_dict2[c] for c in ctr_labels2]
    tar_bit2 = bit_dict2[tar_label2]
    if numctrl2 == 0:
        qasmfile.write('x q['+str(tar_bit2)+'];\n')
    elif numctrl2 == 1:
        qasmfile.write('cx q['+str(ctr_bits2[0])+'], q['+str(tar_bit2)+'];\n')
    elif numctrl2 == 2:
        qasmfile.write('ccx q['+str(ctr_bits2[0])+'], q['+str(ctr_bits2[1])+'], q['+str(tar_bit2)+'];\n')
    else:
        mcx_str2 = '], q['.join(str(bits) for bits in ctr_bits2)
        qasmfile.write('mcx q['+mcx_str2+'], q['+str(tar_bit2)+'];\n')

print('circuit 2 done.')
