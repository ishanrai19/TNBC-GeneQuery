# curate_data.py
# This script performs a one-time setup to process the raw TCGA data files
# into clean, analysis-ready cohorts for our final tool.

import pandas as pd
import os

print("Starting data curation process...")

# --- 1. Define File Paths ---
# These are the names of the files you downloaded.
# Make sure they are in the same directory as this script.
clinical_file = 'TCGA.BRCA.sampleMap_BRCA_clinicalMatrix.tsv'
expression_file = 'HiSeqV2' # The 172MB gene expression file

# --- 2. Load the Clinical and Sample Type Data ---
# The clinical file contains both the receptor status and the sample type information.
try:
    # Set the first column ('sampleID') as the index right away
    clinical_df = pd.read_csv(clinical_file, sep='\t', index_col=0)
except FileNotFoundError:
    print(f"Error: The clinical file '{clinical_file}' was not found.")
    print("Please make sure it is in the same directory as this script.")
    exit()

print("Successfully loaded clinical data.")

# --- 3. Identify the Normal Samples ---
# We will filter the clinical dataframe to find all samples explicitly marked
# as 'Solid Tissue Normal'.
normal_samples_df = clinical_df[clinical_df['sample_type'] == 'Solid Tissue Normal']
# Get the list of sample IDs for the normal cohort from the DataFrame's index.
normal_sample_ids = normal_samples_df.index.tolist()
print(f"Identified {len(normal_sample_ids)} Normal Tissue samples.")


# --- 4. Identify the Triple-Negative Breast Cancer (TNBC) Samples ---
# This is a multi-step filtering process.

# First, get all the primary tumor samples.
primary_tumor_df = clinical_df[clinical_df['sample_type'] == 'Primary Tumor']

# Now, apply the three filters for TNBC based on receptor status.
# The column names are taken directly from the clinical file.
tnbc_samples_df = primary_tumor_df[
    (primary_tumor_df['breast_carcinoma_estrogen_receptor_status'] == 'Negative') &
    (primary_tumor_df['breast_carcinoma_progesterone_receptor_status'] == 'Negative') &
    (primary_tumor_df['lab_proc_her2_neu_immunohistochemistry_receptor_status'] == 'Negative')
]
# Get the list of sample IDs for the TNBC cohort from the DataFrame's index.
tnbc_sample_ids = tnbc_samples_df.index.tolist()
print(f"Identified {len(tnbc_sample_ids)} Triple-Negative (TNBC) samples.")


# --- 5. Process the Gene Expression Matrix ---
# Load the large expression file. It's a tab-separated file.
# We set the first column ('sample') as the index, which contains the gene symbols.
try:
    expression_df = pd.read_csv(expression_file, sep='\t', index_col=0)
except FileNotFoundError:
    print(f"Error: The expression file '{expression_file}' was not found.")
    exit()

print("Successfully loaded gene expression data.")

# The data from UCSC Xena is already log2(x+1) transformed, so we do NOT need to do it again.

# --- 6. Create the Final, Clean DataFrames ---
# Select only the columns that match our identified sample IDs for each cohort.
# We also need to find the common samples between our lists and the expression data columns.
valid_normal_ids = [sid for sid in normal_sample_ids if sid in expression_df.columns]
valid_tnbc_ids = [sid for sid in tnbc_sample_ids if sid in expression_df.columns]

print(f"Found {len(valid_normal_ids)} normal samples and {len(valid_tnbc_ids)} TNBC samples in the expression matrix.")

normal_expression_final = expression_df[valid_normal_ids]
tnbc_expression_final = expression_df[valid_tnbc_ids]


# --- 7. Save the Curated Files ---
# Create a 'data' directory if it doesn't exist.
if not os.path.exists('data'):
    os.makedirs('data')

# Save the final, clean datasets as CSV files. These will be used by our main tool.
normal_expression_final.to_csv('data/normal_expression_log2.csv')
tnbc_expression_final.to_csv('data/tnbc_expression_log2.csv')

print("\nData curation complete!")
print("Two new files have been created in the 'data/' directory:")
print("1. normal_expression_log2.csv")
print("2. tnbc_expression_log2.csv")
print("\nYou are now ready to build the main analysis tool.")