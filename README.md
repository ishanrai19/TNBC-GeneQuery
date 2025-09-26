# TNBC-GeneQuery
# TNBC-GeneQuery: A Transcriptomic Analysis Tool

A command-line tool to automate the analysis of gene expression differences between Triple-Negative Breast Cancer (TNBC) and normal tissue using data from The Cancer Genome Atlas (TCGA).

Prerequisites
Python (version 3.8 or newer)
git

1. Installation
First, clone the repository and install the necessary Python libraries.bash

Clone this repository to your local machine
git clone <your-repository-url>

Navigate into the project directory
cd TNBC-GeneQuery

Install the required Python packages
pip install -r requirements.txt


## 2. One-Time Data Setup

Before using the tool, you must download the source data from the UCSC Xena platform and run the curation script. This only needs to be done once.

**Step 1: Download Data**

Go to the(https://xenabrowser.net/datapages/?cohort=TCGA%20Breast%20Cancer%20(BRCA)&removeHub=https%3A%2F%2Fxena.treehouse.gi.ucsc.edu%3A443) and download the following three files into your `TNBC-GeneQuery` directory:

1.  **Gene Expression:** From the `gene expression RNAseq` section, download `IlluminaHiSeq*`.
2.  **Clinical Data:** From the `phenotype` section, download `Phenotypes`.
3.  **Survival Data:** From the `phenotype` section, download `Curated survival data`.

**Step 2: Run the Curation Script**

Run the `curate_data.py` script from your terminal. This will process the large files and create the clean datasets needed for the analysis tool.

```bash
python curate_data.py
```
This will create a data/ directory containing tnbc_expression_log2.csv and normal_expression_log2.csv.

3. How to Run the Tool
Once the data setup is complete, you can query any gene using the tnbc_gene_query.py script with the --gene flag.

Syntax:
```
python tnbc_gene_query.py --gene <GENE_SYMBOL>
```
Example:
```
python tnbc_gene_query.py --gene BRCA1
```
4. Example Output
Running the command for the gene BRCA1 will produce the following output in your terminal and save a plot to your directory.

Console Output:
```
--- TNBC Gene Expression Explorer ---
Gene Queried: BRCA1
Average Expression (TNBC): 8.13 (log2 scale)
Average Expression (Normal): 7.62 (log2 scale)
Log2 Fold Change (TNBC/Normal): 0.51

Visualization saved to: BRCA1_expression_plot.png
```
