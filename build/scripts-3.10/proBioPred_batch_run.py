#!python

import argparse
import os
import sys
import subprocess
import pandas as pd
import shutil

parser = argparse.ArgumentParser(description="Wrapper for running ProBioPred for batch of genomes. Searches for "
                                             "probiotic, virulent and antibiotic resistence "
                                             "genes in query genomes. Then predicts the probability "
                                             "score of genome being probiotic or non-probiotic "
                                             "based on SVM model.")
parser.add_argument('-b','--batch_file',metavar='PATH',required=True,
                    type=str,help='Genome batch file. (Tab separated with two columns, genomeID, genomeFile and genus). Genus must be from one of the following [bacillus, clostridium, lactobacillus, leuconostoc, streptococcus, '
                         'bifidobacterium, enterococcus, lactococcus, pediococcus]')
parser.add_argument('-o','--output_dir',metavar='PATH',required=False,
                    default='ProBioPred_out',type=str,help='Path of output directory [Default: ProBioPred_out].')
parser.add_argument('-t','--threads',default=1,type=int,
                    help='Number of threads to run for BLAST and RGI.')

args = parser.parse_args()

batch_file = args.batch_file
userFolder = args.output_dir
threads = str(args.threads)

# 1. read and validate batch file
df_batch = pd.read_csv(batch_file,sep='\t')

# 2. validate batch file
if(sum(['genomeID', 'genomeFile', 'genus'] == df_batch.columns) != 3):
    exit('Please validate the column names of batch file. It must be tab separated and should have 3 columns: genomeID, genomeFile, genus')
if(len(set(df_batch['genomeID'])) != df_batch.shape[0]):
    exit('genomIDs must have unique names')

# 3. make directory for output
cwd = os.getcwd()
os.chdir(cwd)
if (os.path.exists(userFolder)):
    flag = input("Directory " + userFolder + " already exists. Enter \"1\" to overwrite or \"0\" to exit. \n")
    if (flag == "1"):
        shutil.rmtree(userFolder)
        os.mkdir(userFolder)
        cwd = os.path.join(cwd,userFolder)
    else:
        exit("Exiting...")
else:
    os.mkdir(userFolder)
    cwd = os.path.join(cwd,userFolder)

# 4. loop over and run probiopred
for genomeId, genomeFile, genus in zip(df_batch['genomeID'], df_batch['genomeFile'], df_batch['genus']):
    genomeId = genomeId.strip()
    genomeFile = genomeFile.strip()
    genus = genus.strip()
    outDir = os.path.join(userFolder,genomeId)
    cmd = 'proBioPred.py -i ' + genomeFile + ' -g ' + genus + ' -o ' + outDir + ' -t ' + threads
    print(cmd)
    subProbiopred = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output,error = subProbiopred.communicate()
    if(subProbiopred.returncode != 0):
        exit(error)

# 5. collect data and make summary
df_list = []
for genome, result in zip(os.listdir(userFolder), [os.path.join(os.getcwd(),userFolder,i,'resulTab.csv') for i in os.listdir(userFolder)]):
    df = pd.read_csv(result, sep='\t')
    df = df[['prediction', 'prediction_score']]
    df['genomeID'] = genome
    df_list.append(df)
df_final = pd.concat(df_list)
df_final.to_csv(os.path.join(userFolder, 'summary_result.tsv'),sep='\t')