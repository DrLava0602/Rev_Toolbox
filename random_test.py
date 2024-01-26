import random
N = 2000
G = 10000
real_file = str(N)+"_"+str(G)+".real"
realfile = open(real_file,'w')
realfile.write('# N = '+str(N)+", G = "+str(G)+"\n")
realfile.write(".numvars "+str(N)+"\n.variables")
for i in range(N):
    realfile.write(" x"+str(i))
realfile.write("\n.inputs")
for i in range(N):
    realfile.write(" x"+str(i))
realfile.write("\n.outputs")
for i in range(N):
    realfile.write(" x"+str(i))
realfile.write("\n.begin\n")
for i in range(9000):
    temp = random.sample(range(10), k=3)
    realfile.write("t3 x"+str(temp[0])+" x"+str(temp[1])+" x"+str(temp[2])+"\n")
for i in range(1000):
    temp = random.sample(range(N), k=3)
    realfile.write("t3 x"+str(temp[0])+" x"+str(temp[1])+" x"+str(temp[2])+"\n")