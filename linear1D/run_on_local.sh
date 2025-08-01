#!/bin/bash

ulimit -s unlimited

export NEKRS_HOME=~/work/software/nekrs_LS_build/nekRS_LS/nekRS/

mpirun --mca osc ucx -np 1 nekrs --setup linear | tee log.dat
