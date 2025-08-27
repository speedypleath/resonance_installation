#!/usr/bin/env python3
"""
EEG Directory to CSV Processor

This script processes a directory containing EEG data files organized in BIDS format
and creates a CSV file with subject information, trial IDs, labels, and file paths.

Directory structure expected:
directory/
|-- sub-ID***
|           |-- ses-S***
|           |         |-- sub-ID***_ses-S***_task-Default_run-001_eeg.json
|           |         |-- sub-ID***_ses-S***_task-Default_run-001_eeg.edf

Output CSV structure:
| subject_id | trial_id | label | file_path |
"""

import os
import json
import csv
import re
from pathlib import Path
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_subject_id(filename_or_path):
    """Extract subject ID from filename or path."""
    match = re.search(r'sub-([^_/\\]+)', str(filename_or_path))
    return match.group(1) if match else None


def extract_session_id(filename_or_path):
    """Extract session ID from filename or path."""
    match = re.search(r'ses-([^_/\\]+)', str(filename_or_path))
    return match.group(1) if match else None


def extract_valence_from_json(json_path):
    """
    Extract valence from JSON file.

    Args:
        json_path: Path to the JSON file
        
    Returns:
        Label extracted from JSON, or None if not found
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Common label fields in EEG JSON files
        # You may need to adjust these based on your specific JSON structure
        description = data.get('TaskDescription', None)
        description = description.split(',')
        avg_valence = float([item for item in description if 'AVG_Valence' in item][0].split(':')[1])

        return avg_valence

    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        logger.error(f"Error reading JSON file {json_path}: {e}")
        return "Error"

def extract_arousal_from_json(json_path):
    """
    Extract arousal from JSON file.

    Args:
        json_path: Path to the JSON file

    Returns:
        Label extracted from JSON, or None if not found
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Common label fields in EEG JSON files
        # You may need to adjust these based on your specific JSON structure
        description = data.get('TaskDescription', None)
        description = description.split(',')
        avg_arousal = float([item for item in description if 'AVG_Arousal' in item][0].split(':')[1])

        return avg_arousal

    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        logger.error(f"Error reading JSON file {json_path}: {e}")
        return "Error"

def process_directory(root_directory, output_csv):
    """
    Process the directory structure and create CSV file.
    
    Args:
        root_directory: Path to the root directory containing subject folders
        output_csv: Path to the output CSV file
    """
    print("Processing directory:", root_directory)
    root_path = Path(root_directory)
    
    if not root_path.exists():
        logger.error(f"Directory {root_directory} does not exist")
        return
    
    results = []
    
    # Pattern to match subject directories
    subject_pattern = re.compile(r'^sub-.*')
    session_pattern = re.compile(r'^ses-.*')
    
    # Walk through the directory structure
    for subject_dir in root_path.iterdir():
        if not (subject_dir.is_dir() and subject_pattern.match(subject_dir.name)):
            continue
            
        subject_id = extract_subject_id(subject_dir.name)
        
        # Look for session directories within subject directory
        for session_dir in subject_dir.iterdir():
            if not (session_dir.is_dir() and session_pattern.match(session_dir.name)):
                continue

            session_id = extract_session_id(session_dir.name)
            session_dir = next(iter(session_dir.iterdir()), None)
            trial_id = f"{session_id}" if session_id else subject_id
            
            # Look for EDF and JSON files in session directory
            edf_files = list(session_dir.glob("*.edf"))
            json_files = list(session_dir.glob("*.json"))
            
            print(f"    Found {len(edf_files)} EDF files and {len(json_files)} JSON files in {session_dir.name}")
            
            # Match EDF files with corresponding JSON files
            for edf_file in edf_files:
                # Find corresponding JSON file
                base_name = edf_file.stem  # filename without extension
                json_file = session_dir / f"{base_name}.json"
                
                if json_file.exists():
                    valence = extract_valence_from_json(json_file)
                    arousal = extract_arousal_from_json(json_file)
                    logger.info(f"    Found pair: {edf_file.name} with valence '{valence}' and arousal '{arousal}'")
                else:
                    # Look for any JSON file in the directory as fallback
                    if json_files:
                        valence = extract_valence_from_json(json_files[0])
                        arousal = extract_arousal_from_json(json_files[0])
                        logger.warning(f"    Using fallback JSON file for {edf_file.name}")
                    else:
                        valence = "No_JSON"
                        arousal = "No_JSON"
                        logger.warning(f"    No JSON file found for {edf_file.name}")
                
                results.append({
                    'subject_id': subject_id,
                    'trial_id': trial_id,
                    'valence': valence,
                    'arousal': arousal,
                    'file_path': str(edf_file.absolute())
                })
    
    # Write results to CSV
    if results:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['subject_id', 'trial_id', 'valence', 'arousal', 'file_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        
        logger.info(f"Successfully created CSV file: {output_csv}")
        logger.info(f"Total entries: {len(results)}")
    else:
        logger.warning("No EDF files found in the directory structure")


def main():
    """Main function to handle command line arguments and run the processor."""
    parser = argparse.ArgumentParser(
        description='Process EEG directory structure and create CSV file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python eeg_processor.py /path/to/eeg_data output.csv
  python eeg_processor.py ./data ./results/eeg_files.csv
        """
    )
    
    parser.add_argument('directory', 
                       help='Root directory containing subject folders')
    parser.add_argument('output_csv', 
                       help='Output CSV file path')
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Process the directory
    process_directory(args.directory, args.output_csv)


if __name__ == "__main__":
    main()