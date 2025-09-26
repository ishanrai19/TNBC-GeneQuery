# tnbc_gene_query.py
# This is the main tool for querying gene expression differences in TNBC.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import sys
import os

def create_parser():
    """Creates and configures the argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Query gene expression in TNBC vs Normal tissue from pre-curated TCGA data."
    )
    parser.add_argument(
        '--gene',
        type=str,
        required=True,
        help='Official gene symbol to query (e.g., BRCA1).'
    )
    return parser

def analyze_gene_expression(gene_symbol):
    """
    Loads the curated data, calculates statistics for the specified gene,
    and prints the results to the console.
    """
    # Define paths to the clean data files
    normal_data_path = 'data/normal_expression_log2.csv'
    tnbc_data_path = 'data/tnbc_expression_log2.csv'

    # Load the pre-curated data files
    try:
        normal_df = pd.read_csv(normal_data_path, index_col=0)
        tnbc_df = pd.read_csv(tnbc_data_path, index_col=0)
    except FileNotFoundError:
        print("Error: Curated data files not found in the 'data/' directory.")
        print("Please ensure you have run the 'curate_data.py' script successfully.")
        sys.exit(1)

    # Check if the requested gene exists in our dataset's index (the gene list)
    if gene_symbol not in tnbc_df.index:
        print(f"Error: Gene '{gene_symbol}' not found in the dataset.")
        print("Please check the spelling and ensure it is an official gene symbol.")
        sys.exit(1)

    # Extract the expression data (a single row) for the specified gene
    normal_expr = normal_df.loc[gene_symbol]
    tnbc_expr = tnbc_df.loc[gene_symbol]

    # Calculate the key statistics
    mean_normal = normal_expr.mean()
    mean_tnbc = tnbc_expr.mean()
    # Standard Error of the Mean (SEM) is used for the error bars in the plot
    sem_normal = normal_expr.sem()
    sem_tnbc = tnbc_expr.sem()
    
    # Calculate Log2 Fold Change: the difference in the mean log2 expression
    log2_fold_change = mean_tnbc - mean_normal

    # Print a clean, formatted summary to the console
    print("\n--- TNBC Gene Expression Explorer ---")
    print(f"Gene Queried: {gene_symbol}")
    print(f"Average Expression (TNBC): {mean_tnbc:.2f} (log2 scale)")
    print(f"Average Expression (Normal): {mean_normal:.2f} (log2 scale)")
    print(f"Log2 Fold Change (TNBC/Normal): {log2_fold_change:.2f}")

    # Return all calculated values in a dictionary for the plotting function
    return {
        'gene': gene_symbol,
        'means': [mean_tnbc, mean_normal],
        'sems': [sem_tnbc, sem_normal],
        'cohorts':['TNBC', 'Normal']
    }

def create_plot(plot_data):
    """
    Generates and saves a publication-quality bar plot of the results.
    """
    plt.figure(figsize=(7, 7))
    sns.set_style("whitegrid")
    
    # Create the bar plot
    bars = plt.bar(
        x=plot_data['cohorts'],
        height=plot_data['means'],
        yerr=plot_data['sems'],  # Add error bars using the SEM
        capsize=10,              # Style for the error bar caps
        color=["#4600b7", "#d26013"], # Assign distinct colors
        alpha=0.9
    )

    # Add labels and a title for clarity
    plt.ylabel("Mean Gene Expression (log2(norm_count + 1))", fontsize=12)
    plt.title(f"Expression of {plot_data['gene']} in TNBC vs. Normal Tissue", fontsize=14, weight='bold')
    plt.xticks(fontsize=12)
    
    # Save the plot to a file
    output_filename = f"{plot_data['gene']}_expression_plot.png"
    plt.savefig(output_filename, dpi=300) # Save as a high-resolution image
    print(f"\nVisualization saved to: {output_filename}")

def main():
    """
    Main function to orchestrate the script's execution.
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Run the analysis
    results = analyze_gene_expression(args.gene)
    # Create the plot from the analysis results
    create_plot(results)

if __name__ == '__main__':
    main()