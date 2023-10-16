[![alt text](logo.png)]

<div style="text-align: justify">
ProBioPred can predict the potential probiotic candidates from genome sequence based on Support Vector Machine (SVM) trained models. Preferable input for ProBioPred is complete genome for better results, but you can also provide draft genome assembly. Currently, ProBioPred supports prediction for only 9 genera viz. <i>Bacillus, Clostridium, Lactobacillus, Leuconostoc, Streptococcus, Bifidobacterium, Enterococcus, Lactococcus</i> and <i>Pediococcus.</i>
The input genome should be in standard FASTA format to run this tool.
</div>

## Theory

The ProBioPred uses available genetic information and Support Vector Machine (SVM) models for prediction of potential probiotic candidate. In brief, based on extensive literature survey and available databases, ProBioPred uses information on genes imparting **probiotic properties**, **virulence factors** and **antibiotic resistance genes** to generate and train models which eventually predicts a potential probiotic candidate. ProBioPred can also serves as a tool to predict probiotic genes, virulence factors and antibiotic resistance genes which can be browsed on the website or downloaded. These models can be used for analysis of genome sequences using ProBioPred either [online](http://210.212.161.142/ProBioPred/) or as a stand-alone tool.

![](https://github.com/microDM/ProBioPred/blob/master/performance.jpeg)


## Installing ProBioPred

```
# create conda environment
conda create -n probiopred python=3.10
conda activate probiopred

# install dependencies
# blast
conda install -c bioconda blast

# libsvm
conda install -c conda-forge libsvm

# install rgi
git clone https://github.com/arpcard/rgi.git
cd rgi
pip install .

# install rgi database
rgi auto_load

# install ProBioPred
git clone https://github.com/microDM/ProBioPred.git
cd ProBioPred
pip install .
```
   
### Running ProBioPred
```
usage: proBioPred.py [-h] -i PATH -g GENUS [-o PATH] [-t THREADS]

Wrapper for running ProBioPred. Searches for probiotic, virulent and
antibiotic resistence genes in query genome. Then predicts the probability
score of genome being probiotic or non-probiotic based on SVM model.

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input_genome PATH
                        Query genome sequence in FASTA format
  -g GENUS, --genus GENUS
                        Genus of query genome. Currently support only
                        following 9 genera.[bacillus, clostridium,
                        lactobacillus, leuconostoc, streptococcus,
                        bifidobacterium, enterococcus, lactococcus,
                        pediococcus]
  -o PATH, --output_dir PATH
                        Path of output directory [Default: ProBioPred_out].
  -t THREADS, --threads THREADS
                        Number of threads to run for BLAST and RGI.
```

### Run ProBioPred on batch of genomes

```
# create tab-separated file with 3 columns:
        1. genomeID: unique genome ID
        2. genomeFile: file path to respective genome (fasta)
        3. genus: one of the genus listed in ProBioPred help.

```

#### Output
ProBioPred generates output directory with several files and prints SVM score for probiotic/non-probiotic on standard output.

|File|Description|
|:----|:------|
|out.libsvm|svm-predict output (1/-1 referes to probiotic/non-probiotic class)|
|pro_hits.pfasta|Probiotic genes (multi-FASTA file)|
|pro_outFiltered.blast|BLAST outfmt6 for probiotic genes|
|resulTab.csv|Scores for each features (.csv format)|
|rgi_out.json|RGI output (json format)|
|rgi_out.txt|RGI output (tab-delimited format)|
|vfdb_hits.pfasta|Virulent genes (mult-FASTA file)|
|vfdb_outFiltered.blast|BLAST outfmt6 for virulent genes|
