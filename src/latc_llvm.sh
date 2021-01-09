#!/usr/bin/env bash

outfile="${*%.ins}.ll"
outfile_bc="${*%.ins}.bc"
if 
source env/bin/activate; \
python3 ./src/main.py "$*";
then
  llvm-as -o out.bc "$outfile"
  llvm-as -o ./lib/runtime.bc ./lib/runtime.ll
  llvm-link -o "$outfile_bc" ./lib/runtime.bc out.bc
  rm out.bc
fi
