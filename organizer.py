import shutil
from pathlib import Path

# mapping extensions to their folders
EXT_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Docs': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.csv'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z']
}

def sort_files(target_dir):
    p = Path(target_dir)
    
    if not p.is_dir():
        print("Bad path. Try again.")
        return

    print(f"Sorting files in {target_dir}...")
    
    for item in p.iterdir():
        # ignore folders and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue

        ext = item.suffix.lower()
        if not ext:
            continue 

        # find the right folder, default to 'Other'
        dest_folder = "Other"
        for folder, extensions in EXT_MAP.items():
            if ext in extensions:
                dest_folder = folder
                break
        
        dest_path = p / dest_folder
        dest_path.mkdir(exist_ok=True)
        
        # handle duplicate file names by appending a number
        final_dest = dest_path / item.name
        counter = 1
        while final_dest.exists():
            final_dest = dest_path / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        try:
            shutil.move(str(item), str(final_dest))
            print(f"Moved: {item.name} -> {dest_folder}/")
        except Exception as e:
            print(f"Couldn't move {item.name}: {e}")

if __name__ == '__main__':
    folder = input("Folder path to organize: ").strip('\"\'')
    sort_files(folder)
    print("Done!")