# Rev_Toolbox - Tools for checking equivlance of reversible circuits

## Introduction
This toolbox is used to convert the .real files to different file types required to run equivalence checking of reversible circuits on either SliQEqc_Rev or the SAT-based method that can be run with cryptominisat.

## Usage
1. r2q_miter.py: convert two .real files into a reversible miter in qasm format.
```
python r2q_miter.py file1.real file2.real
```
2. xorcnf_qasm.py: convert a qasm reversible miter into xor-cnf form
```
python xorcnf_qasm.py file.qasm
```
3. random_test.py: generate random circuits with parameters within the py file
```
python random_test.py
```
5. xorcnf_real.py: convert two .real files into xor-cnf form to check equivalence
```
python xorcnf_real.py file1.real file2.real
```
