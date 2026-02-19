#!/usr/bin/env python3
"""
Smart File Organizer
--------------------------------------------------------------------------------------------
A python script to automatically organize files in a given directory based on file types.
"""

from pathlib import Path
import constants as const
from shutil import move
import logging
from datetime import datetime
import argparse

# ----- CONFIGURATION -----

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

""" 
Path to source folder that needs to be organized. 
Must provide absolute path. Edit this line!!!
"""
source_folder = Path("/Users/estesb1/code/python/python-projects/portfolio/SmartFileOrganizer/files")

""" 
Returns category name from given file extension 
Example .jpg extension -> Images
"""
def get_category(file_suffix):
    for category, extension in const.FILE_TYPES.items():
        if file_suffix in extension:
            return category  
    return "Others"

def build_target_folder(organized_root: Path, file: Path):
    category = get_category(file.suffix)
    
    # Get the file's modified time as a datetime object
    modified_time = datetime.fromtimestamp(file.stat().st_mtime)
    date_folder = modified_time.strftime("%Y-%m")  # e.g., "2025-07"

    # Build the full target path with category and date
    return organized_root / category / date_folder
        

# Iterate through source folder
def organize_files(source_folder: Path, output_root: Path, dryrun: bool=False):
    if not source_folder.exists or not source_folder.is_dir():
        logging.error("The specified source folder either does not exist or is not a directory.")
        return
        
    # Create the organized folder structure
    # organized = source_folder / "Organized"
    output_root.mkdir(parents=True, exist_ok=True)
    
    for item in source_folder.iterdir():
        # print(file.name)
        if item.is_file():
            # category = get_category(item.suffix)
            
            # # Get the file's modified time as a datetime object
            # mod_time = datetime.fromtimestamp(item.stat().st_mtime)
            # date_folder_name = mod_time.strftime("%Y-%m")  # e.g., "2025-07"

            # # Build the full target path with category and date
            # target_folder = organized / category / date_folder_name
            target_folder = build_target_folder(output_root, item)
            target_folder.mkdir(parents=True, exist_ok=True)
            
            try:
                if dryrun:
                    logging.info(f"[DRY RUN MODE] Would move '{item.name}' to '{target_folder}'")
                else: 
                    # Move files from source to destination folder
                    dest_folder = target_folder / item.name
                    move(item, dest_folder)
                    logging.info(f"Moving [{item.name}] to [{target_folder}]\n")
                    logging.info("Organizing complete!")
            except Exception as e:
                logging.error(f"Error moving '[{item.name}]': {e}\n")
                return e

if __name__ == "__main__":
    logging.info("Starting Smart File Organizer...")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dryrun", action="store_true")
    args = parser.parse_args()
    organize_files(dryrun=args.dryrun)
    
    
# TODO Additional Enhancements
# Configurable rules (optional) (categorize by filetype, modification date or size)
# Create a GUI (optional)

