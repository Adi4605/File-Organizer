import shutil
from pathlib import Path

# mapping extensions to their folders
EXT_MAP = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff', '.heic', '.raw'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm'],
    'Docs': ['.pdf', '.docx', '.doc', '.txt', '.xls', '.xlsx', '.csv', '.rtf', '.odt', '.ppt', '.pptx', '.epub'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.opus'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z', '.pkg'],
    'Codes': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.sh', '.json', '.ipynb'],
    'Executables': ['.exe', '.msi', '.dmg', '.deb', '.app'],
    'Fonts': ['.ttf', '.otf', '.woff']
}

def is_project_folder(target_dir):
    """Quick check for common project markers to avoid nuking a codebase."""
    markers = ['.git', 'package.json', 'requirements.txt', 'pom.xml']
    for marker in markers:
        if (target_dir / marker).exists():
            return True
    return False

def sort_files(target_dir):
    p = Path(target_dir)
    
    if not p.is_dir():
        print("Bad path. Try again.")
        return

    # 1. THE DANGER ZONE SAFEGUARD
    if is_project_folder(p):
        print("\nWARNING: This looks like a programming project (found .git or package files).")
        confirm = input("Are you sure you want to run the organizer here? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborting. Your project is safe.")
            return

    print(f"\nSorting files in {target_dir}...")
    
    for item in p.iterdir():
        # 2. THE MAC .APP QUIRK FIX
        # Ignore folders, UNLESS it ends in .app
        if item.is_dir() and item.suffix.lower() != '.app':
            continue
            
        # Ignore hidden files
        if item.name.startswith('.'):
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
        
        # handle duplicate file names
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