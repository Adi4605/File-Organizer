A quick Python utility script to automatically clean up messy folders (like your Downloads folder) by sorting files into categorized subfolders based on their extensions (Images, Videos, Documents, etc.). 

Works on Windows and Linux out of the box.

## Features
- Sorts files by extension into logical folders.
- Unrecognized files just get dumped into an "Other" folder.
- **Safe moving:** Won't overwrite your stuff. If a duplicate file exists, it quickly renames the new one (e.g., `file_1.txt`) so nothing gets lost.
- Uses Python's built-in `pathlib` so it handles file paths perfectly across different operating systems.

## Setup
If you're pulling this down from Git, just clone it and run it. No need for a virtual environment or pip installs.
