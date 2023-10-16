#!/usr/bin/python3

import argparse
import probiopred.probiopred as mydef
import os
import sys
import subprocess
import pandas as pd

parser = argparse.ArgumentParser(description="Wrapper for running ProBioPred. Searches for "
                                             "probiotic, virulent and antibiotic resistence "
                                             "genes in query genome. Then predicts the probability "
                                             "score of genome being probiotic or non-probiotic "
                                             "based on SVM model.")
parser.add_argument('-i','--input_genome',metavar='PATH',required=True,
                    type=str,help='Query genome sequence in FASTA format')
parser.add_argument('-g','--genus',metavar='GENUS',required=True,type=str,
                    help='Genus of query genome. Currently support only following 9 genera.'
                         '[bacillus, clostridium, lactobacillus, leuconostoc, streptococcus, '
                         'bifidobacterium, enterococcus, lactococcus, pediococcus]',
                         choices =['bacillus', 'clostridium', 'lactobacillus', 'leuconostoc', 'streptococcus',
                         'bifidobacterium', 'enterococcus', 'lactococcus', 'pediococcus'])
parser.add_argument('-o','--output_dir',metavar='PATH',required=False,
                    default='ProBioPred_out',type=str,help='Path of output directory [Default: ProBioPred_out].')
parser.add_argument('-t','--threads',default=1,type=int,
                    help='Number of threads to run for BLAST and RGI.')

args = parser.parse_args()

genus = args.genus
genomeFile = str(args.input_genome)
userFolder = args.output_dir
threads = str(args.threads)

try:
    os.mkdir(userFolder,0o777)
    #os.chdir(userFolder)
except:
    exit(userFolder + " already exists.")

# 1. read input
proFile,vfdbFile,model = mydef.readInput(genus)

# 2. makeblastdb
makedbflag = mydef.makeBlastDB(genomeFile, os.path.join(os.getcwd(),userFolder,'genomedb'))
if(makedbflag):
    pass
else:
    exit(makedbflag)

scoreDict = dict()

# 3. Run RGI
rgiResponse,rgiScore = mydef.runRGI(genomeFile, os.path.join(os.getcwd(),userFolder, 'rgi_out'),threads)
if(rgiResponse == True):
    scoreDict["ardb"] = rgiScore
elif(not rgiResponse ==True):
    exit("Failed to run RGI : " + str(rgiResponse))

# 4. blast for virulent genes
if(os.path.isfile(vfdbFile)):
    #do vfdb blast
    if(makedbflag == True):
        blastFlag = mydef.blast(vfdbFile, os.path.join(os.getcwd(),userFolder,'genomedb'), os.path.join(os.getcwd(), userFolder, 'out.blast'))
        #if blast is successful do filtering
        if(blastFlag == True):
            filterFlag = mydef.filterBlastOutput(os.path.join(os.getcwd(), userFolder, 'out.blast'),os.path.join(os.getcwd(), userFolder, 'vfdb_outFiltered.blast'))
            nvfdb = mydef.count_no_of_lines(os.path.join(os.getcwd(), userFolder, 'vfdb_outFiltered.blast'))
            scoreDict["vfdb"] = nvfdb
            #extract sequence
            mydef.extractSeq(mydef.listOfGeneHits(os.path.join(os.getcwd(), userFolder, 'vfdb_outFiltered.blast')),vfdbFile,os.path.join(os.getcwd(), userFolder, 'vfdb_hits.pfasta'))
        else:
            filterFlag = False
            print("Could not filter blast output file : \n" + str(blastFlag))
    else:
        blastFlag = False
        exit("Could not proceed with blast : \n" + str(makedbflag))

# 5. probiotic blast, filtering and creation of scores dictionary
if(makedbflag == True):
    blastFlag = mydef.blast(proFile, os.path.join(os.getcwd(),userFolder,'genomedb'), os.path.join(os.getcwd(), userFolder, 'out.blast'))
    #filter results
    if(blastFlag == True):
        filterFlag = mydef.filterBlastOutput(os.path.join(os.getcwd(), userFolder, 'out.blast'),os.path.join(os.getcwd(), userFolder, 'pro_outFiltered.blast'))
        if(filterFlag ==True):
            #If no probiotic genes found 
            if(mydef.count_no_of_lines(os.path.join(os.getcwd(), userFolder, 'pro_outFiltered.blast')) < 1 ):
                print("Cannot proceed. No probiotic genes found")
                exit(1)
            #add prodict to scoreDict
            scoreDict = scoreDict | mydef.proResults(os.path.join(os.getcwd(), userFolder, 'pro_outFiltered.blast'))
            #extract sequences
            mydef.extractSeq(mydef.listOfGeneHits(os.path.join(os.getcwd(), userFolder, 'pro_outFiltered.blast')),proFile,os.path.join(os.getcwd(), userFolder, 'pro_hits.pfasta'))
        elif(filterFlag ==False):
            print("Could not filter blast output : " + str(blastFlag))
    elif(not blastFlag ==True):
        print("Could not do blast : " + str(blastFlag))

# 6. Prepare libsvm file
mydef.writeResultsToFile(scoreDict, os.path.join(os.getcwd(), userFolder, 'resulTab.csv'))
out = open(os.path.join(os.getcwd(), userFolder, 'resulTab.libsvm'),'w')
out.write('1 ')
df = pd.read_csv(os.path.join(os.getcwd(), userFolder, 'resulTab.csv'),sep=',')
for i,j in enumerate(df.loc[0]):
    out.write(str(i+1)+':'+str(j)+' ')
out.close()

# 7. run prediction
flagPredict = mydef.runPrediction(os.path.join(os.getcwd(), userFolder, 'resulTab.libsvm'),model, os.path.join(os.getcwd(), userFolder, 'out.libsvm'))

# 8. print results
if(flagPredict):
    libSvmOut = open(os.path.join(os.getcwd(), userFolder, 'out.libsvm'),"r")
    predictLines = libSvmOut.readlines()
    scores = predictLines[1].split(" ")
    scorePositive, scoreNegative = scores[1].strip(),scores[2].strip()
    if(scorePositive > scoreNegative):
        print(genomeFile + " is probiotic : " + scorePositive)
        df['prediction'] = 'Probiotic'
        df['prediction_score'] = scorePositive
    else:
        print(genomeFile + " is non-probiotic : " + scoreNegative)
        df['prediction'] = 'Non-Probiotic'
        df['prediction_score'] = scoreNegative
df.to_csv(os.path.join(os.getcwd(), userFolder, 'resulTab.csv'),index=None,sep='\t')
# 9. remove temp files
#mydef.removeTempFiles(genomeFile)
