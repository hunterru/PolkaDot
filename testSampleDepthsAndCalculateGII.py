#!python3

import subprocess
import argparse
import os, sys, re
import gzip, operator,statistics, math

inDir = '/path/to/regionData/'
fileIn = 'test_regionDepths.tsv'

exclude = dict()
counter = 0
with open('regionsToExclude.txt','r') as exIn:
    for lines in exIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            counter += 1
            exclude[counter] = int(lines)

counter = 0
with open(inDir+fileIn,'r') as dataIn:
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
    with open(inDir+fileIn,'r') as dataIn:
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
with open(inDir+fileIn,'r') as dataIn, open('tempNormalizedData.tsv','w') as dataOut:
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

checkMed = list()
with open('tempNormalizedData.tsv','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            lsplit = lines.split()
            checkMed.append(float(lsplit[1]))
print(statistics.median(checkMed))

aveList = list()
with open(inDir+'training_MeanLowerUpper.tsv','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            lsplit = lines.split()
            aveList.append(float(lsplit[0]))

# Adjust for coverage using mean coverage to account for differences between regions
counter = -1
with open('tempNormalizedData.tsv','r') as dataIn, open(fileIn[:-3]+'corrected.tsv','w') as dataOut:
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

# Calculate GII
upperDict = dict()
lowerDict = dict()
counter = 0
with open('lpWGS_controls_training_meanLowerUpper.tsv','r') as dataIn:
    for lines in dataIn:
        lines = lines.rstrip()
        if lines[0] != '#':
            counter += 1
            lsplit = lines.split()
            upperDict[counter] = float(lsplit[2])
            lowerDict[counter] = float(lsplit[1])

sampleList = list()
giiList = list()
for s in range(0,samples):
    GII = 0
    counter = 0
    with open(fileIn[:-3]+'corrected.tsv','r') as dataIn:
        for lines in dataIn:
            lines = lines.rstrip()
            if lines[0] == '#':
                sample = lines.split()
                sampleList.append(sample[s])
            else:
                counter += 1
                lsplit = lines.split()
                if float(lsplit[s]) < lowerDict[counter]:
                    GII += abs(1-float(lsplit[s]))
                elif float(lsplit[s]) > upperDict[counter]:
                    GII += abs(1-float(lsplit[s]))
        giiList.append(GII)

for n in range(0,samples):
    print(sampleList[n],giiList[n])
