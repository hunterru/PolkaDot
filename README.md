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
2. Use "meanDepth_regionBased_1Mbp.py" to calculate for each training sample the average read depth for each region consisting of 1 million consecutive base pairs excluding locations defined by "hg38-blacklistCentroTelo.bed" - locations of telomeres, centromeres, and the ENCODE blacklist to exclude anomalous, unstructured, or high signal regions. The output is two TSV files: (1) 'training_regionDepths.tsv' - region depths from each training sample, (2) 'training_regionLocations.tsv' - coordinates that define each region. This can take a while, so running meanDepth_regionBased_1Mbp.py in a bash script merits consideration.
3. Identify regions to exclude because mean coverage for a specific region from the training set after sample-specific normalization is outside the mean +/- 1.96*SD coverage of all regions. "identifyRegionsToExclude.py" creates a TXT file ('regionsToExclude.txt') from the training set data that marks regions to exclude.
4. Determine the minimum and maximum of "normal" euploid values for each region based on the training set. "generateMinMaxRanges.py" re-normalizes the training set after excluding regions in 'regionsToExclude.txt'. The final euploid copy number model for each regions was defined as the mean +/- 3.891*SD, where 3.891 corresponds to a Z-score of 99.995%. The output is a TSV file containing three columns: (1) mean, (2) lower, and (3) upper value for each region. In the example PolkaDot Plot above, the mean value is the dark gray line at ~1 and the lower and upper values are the light blue lines.

