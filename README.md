# File Organizer

A lightweight, cross-platform utility to instantly clean up messy folders (like your `Downloads` or `Desktop`). It automatically sorts files into subfolders (`Images`, `Videos`, `Docs`, etc.) based on their extensions.

## Features
* **Drag & Drop GUI**: Built with TkinterDnD. Just drop a folder path in and click go.
* **Duplicate Safe**: Automatically renames files (e.g., `image_1.jpg`) instead of accidentally overwriting your stuff.
* **Danger Zone Protection**: Scans for `.git` or `package.json` files and warns you before sorting, so you don't accidentally nuke a coding project.
* **History**: Remembers the last 5 folders you sorted in a handy dropdown menu.

## Download & Run (The Easy Way)
You don't need Python installed to use this. 
1. Go to the **Releases** tab on the right.
2. Download the latest `.zip` for your OS (Windows or Linux).
3. Extract it and double-click the executable to use.

## Run from Source (The Dev Way)
If you want to run or tweak the raw Python code:

1. Clone the repo.
2. Install the drag-and-drop dependency:
   ```bash
   python -m pip install tkinterdnd2
