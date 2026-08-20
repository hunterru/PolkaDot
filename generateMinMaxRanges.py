#!python3

import subprocess
import argparse
import os, sys, re
import gzip, operator,statistics, math

inDir = '/path/to/regionData/'

exclude = dict()
counter = 0
with open(inDir+'regionsToExclude.txt','r') as exIn:
    for lines in exIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            counter += 1
            exclude[counter] = int(lines)

counter = 0
with open(inDir+'training_regionDepths.tsv','r','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if counter == 0:
            if lines[0] == '#':
                lsplit = lines.split()
                samples = len(lsplit)
                counter = 1

# for each sample, determine the median coverage after excluding regions beyond +/- 2*SD of overall mean for that region
medianList = list()
for m in range(0,samples):
    tempList = list()
    counter = 0
    with open(inDir+'training_regionDepths.tsv','r') as dataIn:
        for lines in dataIn:
            lines = lines.rstrip()
            if lines[0] != '#':
                counter += 1
                if exclude[counter] == 0:
                    lsplit = lines.split()
                    tempList.append(float(lsplit[m]))
    medianList.append(statistics.median(tempList))

# normalize each samples regions to the sample median value, and only include non-excluded regions
counter = 0
with open(inDir+'training_regionDepths.tsv','r') as dataIn, open('tempNormalizedData.tsv','w') as dataOut:
    for lines in dataIn:
        lines = lines.rstrip()
        out = ""
        if lines[0] == '#':
            dataOut.write(lines+'\n')
        else:
            counter += 1
            if exclude[counter] == 0:
                lsplit = lines.split()
                for n in range(0,samples):
                    out += str(float(lsplit[n])/medianList[n])+'\t'
                dataOut.write(out+'\n')


with open('tempNormalizedData.tsv','r') as dataIn, open('tempMeanValues.tsv','w') as dataOut:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] == '#':
            dataOut.write('#Mean'+'\n')
        else:
            lsplit = lines.split()
            tempList = list()
            for k in lsplit:
                tempList.append(float(k))
            dataOut.write(str(sum(tempList)/len(tempList))+'\n')

aveList = list()
with open('tempMeanValues.tsv','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            aveList.append(float(lines))

# Adjust for coverage using mean coverage to account for differences between regions
counter = -1
with open('tempNormalizedData.tsv','r') as dataIn, open('tempAveCorrectedData.tsv','w') as dataOut:
    for lines in dataIn:
        lines = lines.rstrip()
        out = ""
        if lines[0] == '#':
            dataOut.write(lines+'\n')
        else:
            counter += 1
            lsplit = lines.split()
            for n in range(0,samples):
                out += str(1+float(lsplit[n])-aveList[counter])+'\t'
            dataOut.write(out+'\n')

# Take log2 value after multiplying by 2, and do statistics for final output
with open('tempAveCorrectedData.tsv','r') as dataIn, open('training_MeanLowerUpper.tsv','w') as dataOut:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] == '#':
            dataOut.write('#MEAN'+'\t'+'LOWER'+'\t'+'UPPER'+'\n')
        else:
            lsplit = lines.split()
            tempList = list()
            for k in lsplit:
                tempList.append(math.log2(2*float(k)))
            MEAN = sum(tempList)/len(tempList)
            stdev = statistics.stdev(tempList)
            LOWER = MEAN - 3.891*stdev
            UPPER = MEAN + 3.891*stdev
            out = str(MEAN)+'\t'+str(LOWER)+'\t'+str(UPPER)
            dataOut.write(out+'\n')
   
