#!/bin/bash
#SBATCH --job-name=lucky_dog
#SBATCH -N 8
#SBATCH --nodelist=node6
#SBATCH --cpus-per-task=1
python 3para2.py