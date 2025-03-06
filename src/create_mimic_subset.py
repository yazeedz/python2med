#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIMIC-III Subset Creator
A script to create a manageable subset of the MIMIC-III database for educational purposes.
This script creates a random sample of 3,000 hospital admissions and extracts all related data.
"""

import pandas as pd
import numpy as np
import os
import zipfile
from datetime import datetime
import random
from tqdm import tqdm
import sys

def get_input_path():
    """Get and validate the input zip file path."""
    while True:
        mimic_zip = input("\nEnter the path to the MIMIC-III zip file (mimic-iii-clinical-database-1.4.zip): ").strip()
        
        if not mimic_zip:  # Allow user to exit
            sys.exit("\nOperation cancelled.")
            
        if not os.path.exists(mimic_zip):
            print(f"\nError: The file {mimic_zip} does not exist.")
            continue
            
        if not mimic_zip.endswith('.zip'):
            print(f"\nError: {mimic_zip} is not a zip file.")
            continue
            
        # Check if the zip file contains required files
        try:
            with zipfile.ZipFile(mimic_zip, 'r') as zip_ref:
                # Get the root directory name from the first file in the zip
                root_dir = zip_ref.namelist()[0].split('/')[0]
                required_files = [
                    f"{root_dir}/ADMISSIONS.csv.gz",
                    f"{root_dir}/PATIENTS.csv.gz",
                    f"{root_dir}/ICUSTAYS.csv.gz"
                ]
                missing_files = [f for f in required_files if f not in zip_ref.namelist()]
                if missing_files:
                    print(f"\nError: The following required files are missing in the zip file:")
                    for f in missing_files:
                        print(f"  - {f}")
                    continue
                return mimic_zip, root_dir
        except zipfile.BadZipFile:
            print(f"\nError: {mimic_zip} is not a valid zip file.")
            continue

def get_output_path():
    """Get and validate the output directory path."""
    while True:
        subset_dir = input("\nEnter the path where you want to save the subset: ").strip()
        
        if not subset_dir:  # Allow user to exit
            sys.exit("\nOperation cancelled.")
            
        if os.path.exists(subset_dir):
            if not os.path.isdir(subset_dir):
                print(f"\nError: {subset_dir} exists but is not a directory.")
                continue
            if os.listdir(subset_dir):
                response = input(f"\nWarning: {subset_dir} is not empty. Continue? (y/n): ").strip().lower()
                if response != 'y':
                    continue
        else:
            try:
                os.makedirs(subset_dir)
            except Exception as e:
                print(f"\nError: Could not create directory {subset_dir}: {str(e)}")
                continue
        
        return subset_dir

def get_sample_size():
    """Get the desired sample size from user."""
    while True:
        try:
            size = input("\nEnter the number of admissions to include (default: 3000): ").strip()
            if not size:  # Use default
                return 3000
            size = int(size)
            if size <= 0:
                print("\nError: Sample size must be positive.")
                continue
            return size
        except ValueError:
            print("\nError: Please enter a valid number.")

def read_csv_gz_from_zip(zip_path, root_dir, file_name, **kwargs):
    """Read a gzipped CSV file from a zip archive into a pandas DataFrame."""
    print(f"Reading {file_name} from zip file...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(f"{root_dir}/{file_name}") as gz_file:
            return pd.read_csv(gz_file, compression='gzip', **kwargs)

def save_df_to_csv(df, subset_dir, file_name):
    """Save DataFrame to CSV in the subset directory."""
    output_path = os.path.join(subset_dir, file_name)
    print(f"Saving {output_path}...")
    df.to_csv(output_path, index=False)
    return output_path

def process_chartevents_chunks(zip_path, root_dir, icustay_ids, itemids, chunksize=100000):
    """Process CHARTEVENTS in chunks to extract vital signs for selected ICU stays."""
    chunks = []
    total_rows = 0
    chunk_count = 0
    
    print("Processing CHARTEVENTS in chunks...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(f"{root_dir}/CHARTEVENTS.csv.gz") as gz_file:
            for chunk in tqdm(pd.read_csv(gz_file, compression='gzip', chunksize=chunksize)):
                chunk_count += 1
                
                # Filter for selected ICU stays and vital sign ITEMIDs
                filtered_chunk = chunk[
                    (chunk['ICUSTAY_ID'].isin(icustay_ids)) & 
                    (chunk['ITEMID'].isin(itemids))
                ]
                
                if not filtered_chunk.empty:
                    chunks.append(filtered_chunk)
                    total_rows += len(filtered_chunk)
    
    if chunks:
        return pd.concat(chunks, ignore_index=True)
    else:
        return pd.DataFrame()

def process_labevents_chunks(zip_path, root_dir, subject_ids, chunksize=100000, max_per_subject=10):
    """Process LABEVENTS in chunks to extract a sample for selected patients."""
    chunks = []
    total_rows = 0
    subject_counts = {subject_id: 0 for subject_id in subject_ids}
    
    print("Processing LABEVENTS in chunks...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(f"{root_dir}/LABEVENTS.csv.gz") as gz_file:
            for chunk in tqdm(pd.read_csv(gz_file, compression='gzip', chunksize=chunksize)):
                # Filter for selected patients
                filtered_chunk = chunk[chunk['SUBJECT_ID'].isin(subject_ids)]
                
                if not filtered_chunk.empty:
                    # For each patient, take only up to max_per_subject lab events
                    selected_rows = []
                    for _, row in filtered_chunk.iterrows():
                        subject_id = row['SUBJECT_ID']
                        if subject_counts[subject_id] < max_per_subject:
                            selected_rows.append(row)
                            subject_counts[subject_id] += 1
                    
                    if selected_rows:
                        chunks.append(pd.DataFrame(selected_rows))
                        total_rows += len(selected_rows)
                
                # Check if we've reached the limit for all patients
                if all(count >= max_per_subject for count in subject_counts.values()):
                    break
    
    if chunks:
        return pd.concat(chunks, ignore_index=True)
    else:
        return pd.DataFrame()

def create_subset(mimic_zip, subset_dir, sample_size=3000):
    """Create a subset of the MIMIC-III database."""
    try:
        # Set random seed for reproducibility
        np.random.seed(42)
        random.seed(42)
        
        # Validate inputs and get root directory name
        root_dir = validate_inputs(mimic_zip, subset_dir)
        
        # Create plots directory
        plots_dir = os.path.join(subset_dir, "_plots")
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        
        print("\nStarting MIMIC-III subset creation...")
        print(f"Input zip file: {mimic_zip}")
        print(f"Output directory: {subset_dir}")
        print(f"Sample size: {sample_size} admissions")
        print("="*80 + "\n")
        
        # Load key tables
        admissions = read_csv_gz_from_zip(mimic_zip, root_dir, "ADMISSIONS.csv.gz")
        patients = read_csv_gz_from_zip(mimic_zip, root_dir, "PATIENTS.csv.gz")
        icustays = read_csv_gz_from_zip(mimic_zip, root_dir, "ICUSTAYS.csv.gz")
        
        # Create random subset
        print(f"\nSelecting {sample_size} random hospital admissions...")
        all_hadm_ids = admissions['HADM_ID'].unique()
        sampled_hadm_ids = np.random.choice(all_hadm_ids, size=sample_size, replace=False)
        
        # Filter main tables
        admissions_subset = admissions[admissions['HADM_ID'].isin(sampled_hadm_ids)].copy()
        sampled_subject_ids = admissions_subset['SUBJECT_ID'].unique()
        patients_subset = patients[patients['SUBJECT_ID'].isin(sampled_subject_ids)].copy()
        icustays_subset = icustays[icustays['HADM_ID'].isin(sampled_hadm_ids)].copy()
        
        # Get ICU stay IDs
        sampled_icustay_ids = icustays_subset['ICUSTAY_ID'].unique()
        
        # Load and filter other tables
        print("\nExtracting related data...")
        diagnoses = read_csv_gz_from_zip(mimic_zip, root_dir, "DIAGNOSES_ICD.csv.gz")
        diagnoses_subset = diagnoses[diagnoses['HADM_ID'].isin(sampled_hadm_ids)].copy()
        
        procedures = read_csv_gz_from_zip(mimic_zip, root_dir, "PROCEDURES_ICD.csv.gz")
        procedures_subset = procedures[procedures['HADM_ID'].isin(sampled_hadm_ids)].copy()
        
        prescriptions = read_csv_gz_from_zip(mimic_zip, root_dir, "PRESCRIPTIONS.csv.gz")
        prescriptions_subset = prescriptions[prescriptions['HADM_ID'].isin(sampled_hadm_ids)].copy()
        
        # Load dictionary tables
        d_icd_diagnoses = read_csv_gz_from_zip(mimic_zip, root_dir, "D_ICD_DIAGNOSES.csv.gz")
        d_icd_procedures = read_csv_gz_from_zip(mimic_zip, root_dir, "D_ICD_PROCEDURES.csv.gz")
        d_items = read_csv_gz_from_zip(mimic_zip, root_dir, "D_ITEMS.csv.gz")
        d_labitems = read_csv_gz_from_zip(mimic_zip, root_dir, "D_LABITEMS.csv.gz")
        
        # Define vital sign ITEMIDs
        vital_sign_itemids = [
            211, 220045,  # Heart rate
            51, 442, 455, 6701, 220179, 220050,  # Systolic BP
            8368, 8440, 8441, 8555, 220180, 220051,  # Diastolic BP
            223761, 678, 679, 223762,  # Temperature
            615, 618, 220210, 224690  # Respiratory rate
        ]
        
        # Extract vital signs from CHARTEVENTS
        chartevents_subset = process_chartevents_chunks(
            mimic_zip,
            root_dir,
            sampled_icustay_ids,
            vital_sign_itemids
        )
        
        # Extract lab events
        labevents_subset = process_labevents_chunks(
            mimic_zip,
            root_dir,
            sampled_subject_ids,
            max_per_subject=20
        )
        
        # Save all subset DataFrames
        print("\nSaving subset files...")
        save_df_to_csv(admissions_subset, subset_dir, "ADMISSIONS.csv")
        save_df_to_csv(patients_subset, subset_dir, "PATIENTS.csv")
        save_df_to_csv(icustays_subset, subset_dir, "ICUSTAYS.csv")
        save_df_to_csv(diagnoses_subset, subset_dir, "DIAGNOSES_ICD.csv")
        save_df_to_csv(procedures_subset, subset_dir, "PROCEDURES_ICD.csv")
        save_df_to_csv(prescriptions_subset, subset_dir, "PRESCRIPTIONS.csv")
        save_df_to_csv(chartevents_subset, subset_dir, "CHARTEVENTS_VITALS.csv")
        save_df_to_csv(labevents_subset, subset_dir, "LABEVENTS_SAMPLE.csv")
        
        # Save dictionary tables
        save_df_to_csv(d_icd_diagnoses, subset_dir, "D_ICD_DIAGNOSES.csv")
        save_df_to_csv(d_icd_procedures, subset_dir, "D_ICD_PROCEDURES.csv")
        save_df_to_csv(d_items, subset_dir, "D_ITEMS.csv")
        save_df_to_csv(d_labitems, subset_dir, "D_LABITEMS.csv")
        
        # Create README
        readme_content = f"""# MIMIC-III Subset

This directory contains a subset of the MIMIC-III database created for educational purposes.

## Dataset Information

- **Original Source**: MIMIC-III Clinical Database v1.4
- **Subset Creation Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Sample Size**: {sample_size} randomly selected hospital admissions

## Contents

1. **ADMISSIONS.csv**: {admissions_subset.shape[0]} rows, {admissions_subset.shape[1]} columns
2. **PATIENTS.csv**: {patients_subset.shape[0]} rows, {patients_subset.shape[1]} columns
3. **ICUSTAYS.csv**: {icustays_subset.shape[0]} rows, {icustays_subset.shape[1]} columns
4. **DIAGNOSES_ICD.csv**: {diagnoses_subset.shape[0]} rows, {diagnoses_subset.shape[1]} columns
5. **PROCEDURES_ICD.csv**: {procedures_subset.shape[0]} rows, {procedures_subset.shape[1]} columns
6. **PRESCRIPTIONS.csv**: {prescriptions_subset.shape[0]} rows, {prescriptions_subset.shape[1]} columns
7. **CHARTEVENTS_VITALS.csv**: {chartevents_subset.shape[0]} rows, {chartevents_subset.shape[1]} columns
8. **LABEVENTS_SAMPLE.csv**: {labevents_subset.shape[0]} rows, {labevents_subset.shape[1]} columns

## Dictionary Tables

1. **D_ICD_DIAGNOSES.csv**: {d_icd_diagnoses.shape[0]} rows, {d_icd_diagnoses.shape[1]} columns
2. **D_ICD_PROCEDURES.csv**: {d_icd_procedures.shape[0]} rows, {d_icd_procedures.shape[1]} columns
3. **D_ITEMS.csv**: {d_items.shape[0]} rows, {d_items.shape[1]} columns
4. **D_LABITEMS.csv**: {d_labitems.shape[0]} rows, {d_labitems.shape[1]} columns

## Statistics

- Number of unique patients: {patients_subset['SUBJECT_ID'].nunique()}
- Number of unique hospital admissions: {admissions_subset['HADM_ID'].nunique()}
- Number of unique ICU stays: {icustays_subset['ICUSTAY_ID'].nunique()}

## Notes

- This subset maintains the same structure and relationships as the original MIMIC-III database
- CHARTEVENTS has been filtered to include only vital signs
- LABEVENTS includes up to 20 lab tests per patient
"""
        
        # Save README
        with open(os.path.join(subset_dir, "README.md"), 'w') as f:
            f.write(readme_content)
        
        print("\nSubset creation completed successfully!")
        print(f"Output directory: {subset_dir}")
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("MIMIC-III Subset Creator")
    print("="*80)
    
    try:
        # Get input and output paths
        mimic_zip, root_dir = get_input_path()
        subset_dir = get_output_path()
        sample_size = get_sample_size()
        
        # Create the subset
        success = create_subset(mimic_zip, subset_dir, sample_size)
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 