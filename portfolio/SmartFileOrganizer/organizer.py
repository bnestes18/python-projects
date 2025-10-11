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

# Iterate through source folder
def organize_files():
    if not source_folder.exists or not source_folder.is_dir():
        logging.error("The specified source folder either does not exist or is not a directory.")
        return
        
    # Create the organized folder structure
    organized = source_folder / "Organized"
    organized.mkdir(parents=True, exist_ok=True)
    
    for item in source_folder.iterdir():
        # print(file.name)
        if item.is_file():
            category = get_category(item.suffix)
            # Create category folder under source folder directory
            # TODO Create dry-run mode: List all files moves in a list, loop through list and print each line.
            target_folder = organized / category
            target_folder.mkdir(parents=True, exist_ok=True)
            
            # Define destination path
            dest_folder = target_folder / item.name
            try:
                # Move files from source to destination folder
                move(item, dest_folder)
                logging.info(f"Moving {item.name} to {dest_folder}\n")
            except Exception as e:
                logging.error(f"Error moving '{item.name}': {e}\n")

organize_files()
# TODO Additional Enhancements
# Configurable rules (optional) (categorize by filetype, modification date or size)
# Create a GUI (optional)

