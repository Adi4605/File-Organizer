import shutil
import json
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

HISTORY_FILE = Path(__file__).parent / ".recent_paths.json"

def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_history(paths):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(paths[:5], f) # keep only the last 5 paths

def is_project_folder(target_dir):
    """Quick check for common project markers to avoid nuking a codebase."""
    markers = ['.git', 'package.json', 'requirements.txt', 'pom.xml']
    for marker in markers:
        if (target_dir / marker).exists():
            return True
    return False

def sort_files(target_dir):
    # for linux path using '~' sign
    p = Path(target_dir).expanduser().resolve()
    
    if not p.is_dir():
        print(f"Bad path: {p}. Try again.")
        return None

    if is_project_folder(p):
        print("\nWARNING: This looks like a programming project (found .git or package files).")
        confirm = input("Are you sure you want to run the organizer here? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborting. Your project is safe.")
            return None

    print(f"\nSorting files in {p}...")
    
    for item in p.iterdir():
        # ignore folders UNLESS it ends in .app
        if item.is_dir() and item.suffix.lower() != '.app':
            continue
            
        # ignore hidden files
        if item.name.startswith('.'):
            continue

        ext = item.suffix.lower()
        if not ext:
            continue 

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
            
    return str(p)

if __name__ == '__main__':
    history = load_history()
    
    if history:
        print("\nRecent folders:")
        for i, path in enumerate(history, 1):
            print(f"[{i}] {path}")
        print("[0] Enter a new path")
        
        choice = input("\nSelect a number, or just paste a new path: ").strip('\"\'')
        
        if choice.isdigit() and 1 <= int(choice) <= len(history):
            folder = history[int(choice) - 1]
        elif choice == '0':
            folder = input("Folder path to organize: ").strip('\"\'')
        else:
            folder = choice
    else:
        folder = input("Folder path to organize (e.g., ~/Downloads): ").strip('\"\'')

    # THE FIX: Keep asking until they actually type something
    while not folder:
        print("You didn't enter anything!")
        folder = input("Please enter a valid folder path: ").strip('\"\'')

    # Run the organizer and update history if successful
    success_path = sort_files(folder)
    
    if success_path:
        if success_path in history:
            history.remove(success_path)
        history.insert(0, success_path)
        save_history(history)
        
    print("Done!")