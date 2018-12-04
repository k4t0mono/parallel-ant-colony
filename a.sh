#!/bin/bash
echo "Bash version ${BASH_VERSION}..."
for i in {0..9}
  do 
     time mpirun -np 2 python3 main.py test/pr76 100 30 1 3 0.5 $i
     echo "\n\n****\n\n"
 done