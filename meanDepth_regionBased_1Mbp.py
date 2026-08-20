#!python3

import subprocess
import argparse
import os, sys, re
import gzip, operator,statistics

## Location of MPILEUP from singleton consensus sequence collapse
inDir = '/path/to/mpile/'

## Location to output files
outDir = '/path/to/regionData/'

## List of files to process
mpile = ['12345X1', '12345X2', '12345X3']

## Region size is 1 million bp
regSize = 1000000

wgRegCounter = 0 # to follow the number of regSize regions being analyzed across the entire genome
wgRegCounterStart = 1
chrom = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','X']
with open(outDir+'regionDepths.tsv','w') as dataOut, open(outDir+'regionLocations.tsv','w') as regionsOut:
	for ch in chrom:
		controlRegionDepths = dict() # dictionary the uses wgRegCounter as a key to save depths from each region from all samples

		cmdLine = "awk '$1 == \"{}\"' {} > {}".format(ch,'hg38-blacklistCentroTelo.bed','tempBlack.bed')
		cmdLine_run = subprocess.run(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		totalReg = 0
		regDict = dict() # dictionary of region associated with the current chromosome
		with open('tempBlack.bed','r') as blackIn:
			for lines in blackIn:
				lines = lines.rstrip()
				lsplit = lines.split()
				totalReg += 1
				regDict[totalReg] = lsplit[1]+','+lsplit[2]

		reg1Mdict = dict() # dictionary of subregions that span regSize (e.g., 1,000,000 bp)
		for reg in range(1,totalReg):
			temp1 = regDict[reg]
			temp2 = temp1.split(',')
			start = int(temp2[1])
			temp3 = regDict[reg+1]
			temp4 = temp3.split(',')
			stop = int(temp4[0])
			if start+regSize < stop:
				startPos = start + 1
				stopPos = start + regSize + 1
				while stopPos < stop:
					wgRegCounter += 1
					regionsOut.write(str(wgRegCounter)+'\t'+ch+'\t'+str(startPos)+'\t'+str(stopPos)+'\n')
					for bp in range(startPos,stopPos):
						if wgRegCounter in reg1Mdict:
							reg1Mdict[wgRegCounter].append(bp)
						else:
							reg1Mdict[wgRegCounter] = list()
							reg1Mdict[wgRegCounter].append(bp)
					startPos = stopPos
					stopPos += (regSize + 1)
		
		for m in mpile:
			cmdLine = "awk '$1 == \"{}\"' {} > {}".format(ch,inDir+m+'.wgs.mpileup','tempChr.mpile')
			cmdLine_run = subprocess.run(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			posDict = dict() # each key is coordinate specific to each sample; the depth at that coordinate is the entry
			with open('tempChr.mpile','r') as mIn:
				for lines in mIn:
					lines = lines.rstrip()
					lsplit = lines.split()
					posDict[int(lsplit[1])] = int(lsplit[3])
	
			for keys in reg1Mdict:	# all samples will see the same position
				POS = reg1Mdict[keys]  # POS is a list of coordinates associated with a region
				depth = 0
				counts = 0
				for p in POS:
					counts += 1
					if p in posDict:
						depth += posDict[p]
				if keys in controlRegionDepths:
					controlRegionDepths[keys].append(round(float(depth/counts),2))
				else:
					controlRegionDepths[keys] = list()
					controlRegionDepths[keys].append(round(float(depth/counts),2))

		for outK in range(wgRegCounterStart,wgRegCounter+1):
			depthOut = controlRegionDepths[outK]
			dcounter = 0
			for d in depthOut:
				if dcounter == 0:
					dout = str(d)
					dcounter = 1
				else:
					dout += ','+str(d)	
			out = str(outK)+'\t'+dout
			dataOut.write(out+'\n')

		wgRegCounterStart = wgRegCounter+1						
