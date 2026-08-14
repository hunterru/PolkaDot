# PolkaDot
PolkaDot is a training-based low-pass whole genome sequencing algorithm (LP-WGS; 1.4X) that produces genome-wide plots (PolkaDot plots) of copy number variations and quantifies genomic instability (GII = genomic instability index). The name 'PolkaDot' is an homage to the pink polkadot jersey worn by the King (Queen) of the Mountain during the Tour de France (Femmes) since the plots are reminiscent of mountainous terrain.
<img width="1352" height="181" alt="Screenshot 2026-08-13 at 4 07 46 PM" src="https://github.com/user-attachments/assets/b3994302-00e0-4735-8c6e-07c73ebff6c4" />
**Rationale:** PolkaDot enables the mapping and quantitation of genomic instability regardless of available quantity (i.e., picograms to micrograms). Because GII is a continuous metric, rather than categorical, results can be compared within (i.e., serial samples) and between individuals.

## Software Requirements
- FGBIO (https://github.com/fulcrumgenomics/fgbio)
- SAMTOOLS (https://www.htslib.org/)
- PYTHON3

## NGS Data
PolkaDot was written for short-read Illumina data. The provided scripts use paired-end FASTQ (151x151) files generated from PCR-amplified libraries using adapters with dual index, dual unique molecular identifiers (UMIs; 3mers) obtained from IDT.  
  
The dataset must include DNA from young, healthy controls to model region-specific mapping governed by the workflow and sample type used to generate the FASTQ files. The number of samples to include in the training set is undefined, but more is better (e.g., >10). The training samples should be of the same type as the testing samples. For example, do not use buffy DNA to model cell-free DNA, do not use enzymatically sheared DNA to model mechanically sheared DNA, etc. All samples should derive from the same NGS workflow (i.e., library prep) and sequencer.

## Use Instructions
1. Generate MPILEUP from deduplicated BAM files using FASTQ files trimmed to 30 million total paired reads. The attached script uses FGBIO to generate singleton collapsed consensus sequences. However, a standard deduplication tool (e.g., PICARD, removeduplicates) may works similarly as well.
2. 
