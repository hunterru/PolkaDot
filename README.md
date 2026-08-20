# PolkaDot
PolkaDot is a training-based low-pass whole genome sequencing algorithm (LP-WGS; 1.4X) that produces genome-wide plots (PolkaDot plots) of copy number variations and quantifies genomic instability (GII = genomic instability index). The name 'PolkaDot' is an homage to the pink polkadot jersey worn by the King (Queen) of the Mountain during the Tour de France (Femmes) since the plots are reminiscent of mountainous terrain.  
<img width="1269" height="324" alt="PolkaDotPlotForGitHub" src="https://github.com/user-attachments/assets/a35647e9-a0b1-4e3a-a680-c2e3868868b3" />

**Rationale:** PolkaDot enables the mapping and quantitation of genomic instability regardless of available quantity (i.e., picograms to micrograms). Because GII is a continuous metric, rather than categorical, results can be compared within (i.e., serial samples) and between individuals.

## Software Requirements
- FGBIO (https://github.com/fulcrumgenomics/fgbio)
- SAMTOOLS (https://www.htslib.org/)
- PICARD (https://broadinstitute.github.io/picard/)
- PYTHON3 (https://www.python.org/downloads/)
- PIGZ (https://github.com/madler/pigz)

## NGS Data
PolkaDot was written for short-read Illumina data. The provided scripts use paired-end FASTQ (151x151) files generated from PCR-amplified libraries using adapters with dual index, dual unique molecular identifiers (UMIs; 3mers) obtained from IDT. Using long-read technology and/or other adapters will require adaption of the provided code. Honestly, the provided code is just an example. All users, if any, will need to adapt the code to their specific application. This is not a plug-and-play setup.  
  
The dataset must include DNA from young, healthy controls to model region-specific mapping governed by the workflow and sample type used to generate the FASTQ files. The number of samples to include in the training set is undefined, but more is better (e.g., >10). The training samples should be of the same type as the testing samples. For example, do not use buffy DNA to model cell-free DNA, do not use enzymatically sheared DNA to model mechanically sheared DNA, etc. All samples should derive from the same NGS workflow (i.e., library prep) and sequencer.

## Use Instructions
1. Generate MPILEUP from deduplicated BAM files using FASTQ files trimmed to 30 million total paired reads. "callSingletonConsensus_30millionTPR.sh" is a bash script that uses FGBIO to generate singleton (not duplex) collapsed consensus sequences. However, a standard deduplication tool (e.g., PICARD, MarkDuplicates) may work similarly as well.
2. Use "meanDepth_regionBased_1Mbp.py" to calculate for each training sample the average read depth for each region consisting of 1 million consecutive base pairs excluding locations defined by "hg38-blacklistCentroTelo.bed" - locations of telomeres, centromeres, and the ENCODE blacklist to exclude anomalous, unstructured, or high signal regions.

