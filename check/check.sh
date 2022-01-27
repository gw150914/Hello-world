#!/bin/bash
#SBATCH --job-name=lucky_dog
#SBATCH -N 1
#SBATCH --nodelist=node20
#SBATCH --cpus-per-task=1
python check.py