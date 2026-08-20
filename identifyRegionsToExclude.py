#!python3

import subprocess
import argparse
import os, sys, re
import gzip, operator,statistics, math

inDir = '/path/to/regionData/'

# determine the number of samples
counter = 0
with open(inDir+'training_regionDepths.tsv','r') as dataIn:
    for lines in dataIn:
        if counter == 0:
            lines = lines.rstrip()
            if lines[0] == '#':
                lsplit = lines.split()
                samples = len(lsplit)
                counter = 1

# for each sample, determine the median coverage across the genome
medianList = list()
for m in range(0,samples):
    tempList = list()
    counter = 0
    with open(inDir+'training_regionDepths.tsv','r') as dataIn:
        for lines in dataIn:
            lines = lines.rstrip()
            if lines[0] != '#':
                lsplit = lines.split()
                tempList.append(float(lsplit[m]))
    medianList.append(statistics.median(tempList))

# normalize each sample's regions to the sample's median value
counter = 0
with open(inDir+'training_regionDepths.tsv','r') as dataIn, open('tempNormalizedData.tsv','w') as dataOut:
    for lines in dataIn:
        lines = lines.rstrip()
        out = ""
        if lines[0] == '#':
            dataOut.write(lines+'\n')
        else:
            lsplit = lines.split()
            for n in range(0,samples):
                out += str(float(lsplit[n])/medianList[n])+'\t'
            dataOut.write(out+'\n')

counter = 0
aveList = list()
with open('tempNormalizedData.tsv','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            lsplit = lines.split()
            tempList = list()
            for k in lsplit:
                tempList.append(float(k))
            # removes input from regions with zero or excessive coverage
            if sum(tempList)/len(tempList) != 0 and sum(tempList)/len(tempList) < 3:
                aveList.append(sum(tempList)/len(tempList))

MEAN = sum(aveList)/len(aveList)
SD = statistics.stdev(aveList)
UPPER = MEAN + 1.96*SD
LOWER = MEAN - 1.96*SD
with open(inDir+'regionsToExclude.txt','w') as dataOut:
    dataOut.write('#EXCLUDE\n')
    with open('tempNormalizedData.tsv','r') as dataIn:
        for lines in dataIn:
            lines = lines.rstrip()
            if lines[0] != '#':
                lsplit = lines.split()
                tempList = list()
                for k in lsplit:
                    tempList.append(float(k))
                if sum(tempList)/len(tempList) > LOWER and sum(tempList)/len(tempList) < UPPER:
                    dataOut.write('0\n')
                else:
                    dataOut.write('1\n')
