# PolkaDot
PolkaDot is a training-based low-pass whole genome sequencing algorithm (LP-WGS) that produces genome-wide plots (PolkaDot plots) of copy number variations and quantifies genomic instability (GII = genomic instability index). The name 'PolkaDot' is an homage to the pink polkadot jersey worn by the King (Queen) of the Mountain during the Tour de France (Femmes) since the plots are reminiscent of mountainous terrain.
<img width="1352" height="181" alt="Screenshot 2026-08-13 at 4 07 46 PM" src="https://github.com/user-attachments/assets/b3994302-00e0-4735-8c6e-07c73ebff6c4" />
**Rationale:** PolkaDot enables the mapping and quantitation of genomic instability regardless of available quantity (i.e., picograms to micrograms). Because GII is a continuous metric, rather than categorical, results can be compared within (i.e., serial samples) and between individuals.

## Software Requirements
FGBIO (https://github.com/fulcrumgenomics/fgbio)
SAMTOOLS (https://www.htslib.org/)
PYTHON3

## NGS DATA
PolkaDot was written for short-read Illumina data. The provided scripts use paired-end FASTQ (151x151) files generated from PCR-amplified libraries using dual index, dual unique molecular identifiers (UMIs) obtained from IDT. 
