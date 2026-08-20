#!/bin/bash

## --- enter appropriate BASH script info ---

#SBATCH --account=yourAccount
#SBATCH --partition=yourPartition
#SBATCH --time=3-00:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=100000M
#SBATCH -o slurm-%j.out-%N

set -e

export CPU=`getconf _NPROCESSORS_ONLN`
echo $CPU

## --- location of input ---
export WORKDIR=/$USER/script/folder
export FASTQDIR=/fastq/folder

export REF=/path/to/GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly.fa
export FGBIO=/path/to/fgbio/target/scala-2.13/fgbio-2.1.1-cbbef4a-SNAPSHOT.jar
export PICARD=/path/to/picard/build/libs/picard.jar

## --- location of output ---
export BAMDIR=/path/to/output/lpWGS/bams
export MPILEDIR=/path/to/output/lpWGS/mpile

## --- location and creation of scratch ---
export SCRDIR=/scratch/$USER/$SLURM_JOB_ID
mkdir -p $SCRDIR

cd $SCRDIR 
## load tools if available, otherwise, download and export as above with FGBIO, PICARD
module load samtools
module load bwa
module load pigz

for FILENAME in 12345X1	12345X2	12345X3
do
	## Trim FASTQ files to 30 millition TPR
	zcat $FASTQDIR/"$FILENAME"_*_R1_*.fastq.gz | head -n 120000000 > R1.fastq
	pigz R1.fastq

	zcat $FASTQDIR/"$FILENAME"_*_R2_*.fastq.gz | head -n 120000000 > R2.fastq
	pigz R2.fastq

	## Use fgbio to create an unmapped bam for fastq.gz files
	java -Xmx100G -jar $FGBIO --tmp-dir . FastqToBam --input R1.fastq.gz R2.fastq.gz --read-structure 3M2S146T 3M2S146T --output unmapped.bam --sample sample1 --library library1

	## Cleanup
	rm R1.fastq.gz R2.fastq.gz

	## Convert the unmapped bam file to a fastq file
	java -Xmx100G -jar $PICARD SamToFastq -I unmapped.bam -F unmapped.fastq -INTERLEAVE true --TMP_DIR .

	## Map fastq file
	bwa mem -t 14 -p $REF unmapped.fastq | samtools view -S -@ 14 -b - > mapped.bam

	## Cleanup
	rm unmapped.fastq

	## Use Picard tools to sort files based on query name
	java -Xmx100G -jar $PICARD SortSam -I unmapped.bam -O unmapped.sorted.bam -SO queryname --TMP_DIR .

	## Cleanup
	rm unmapped.bam

	## Use Picard MergeBamAlignments to insert the UMI data into the mapped bam file
	java -Xmx100G -jar $PICARD MergeBamAlignment -UNMAPPED unmapped.sorted.bam -ALIGNED mapped.bam --CREATE_INDEX true -O mapped.merged.bam -R $REF --TMP_DIR .

	## Cleanup
	rm unmapped.sorted.bam mapped.bam

	## Single Consensus
	java -Xmx100G -jar $FGBIO --tmp-dir . GroupReadsByUmi --input mapped.merged.bam --output mapped.merged.grouped.bam --strategy adjacency --edits 1 --min-map-q 20 

	## Cleanup
	rm mapped.merged.bam mapped.merged.bai

	## Call Single Consensus
	java -Xmx100G -jar $FGBIO --tmp-dir . CallMolecularConsensusReads --input mapped.merged.grouped.bam --output consensus.single.unaligned.bam --error-rate-post-umi 30 --min-reads 1 --threads 14

	## Cleanup
	rm mapped.merged.grouped.bam

	## .consensus.duplex.unaligned.bam is an unaligned bam file. This can be passed to Rufus and/or aligned to capture read depth.
	## Make a fastq file from the unmapped consensus bam file
	java -Xmx100G -jar $PICARD SamToFastq -I consensus.single.unaligned.bam -F consensus.fastq -INTERLEAVE true --TMP_DIR . 

	## Align the new fastq file
	bwa mem -t 14 -p $REF consensus.fastq | samtools view -S -@ 12 -b - > consensus.mapped.bam

	## Cleanup
	rm consensus.fastq

	## Use Picard tools to sort files based on query name
	java -Xmx100G -jar $PICARD SortSam -I consensus.single.unaligned.bam -O consensus.unmapped.sorted.bam -SO queryname --TMP_DIR .

	## Now merge the consensus mapped bam with the unmapped bam that has the UMI info
	java -Xmx100G -jar $PICARD MergeBamAlignment -UNMAPPED consensus.unmapped.sorted.bam -ALIGNED consensus.mapped.bam --CREATE_INDEX true -O consensus.mapped.merged.bam -R $REF --TMP_DIR .

	## Cleanup
	rm consensus.mapped.bam consensus.unmapped.sorted.bam

	## Now sort and index the file based on coordinated position using Samtools
	samtools sort -@ 14 -o "$FILENAME".consensus.single.aligned.bam consensus.mapped.merged.bam
	samtools index -@ 14 "$FILENAME".consensus.single.aligned.bam
	mv "$FILENAME".consensus.single.aligned.bam.bai "$FILENAME".consensus.single.aligned.bai

	## Create mpileup
	samtools mpileup -B -q 20 -d 1000000 -f $REF -o $MPILEDIR/"$FILENAME".wgs.mpileup "$FILENAME".consensus.single.aligned.bam

	## Cleanup
	rm consensus.mapped.merged.ba*
	mv "$FILENAME".consensus.single.aligned.bam $BAMDIR/
	mv "$FILENAME".consensus.single.aligned.bai $BAMDIR/
done

cd $WORKDIR
rm -rf $SCRDIR
