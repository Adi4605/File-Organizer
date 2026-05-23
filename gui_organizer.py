import shutil
import json
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from tkinterdnd2 import TkinterDnD, DND_FILES

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

HISTORY_FILE = Path.home() / ".file_organizer_history.json"

class OrganizerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("600x450")

        self.history = self.load_history()
        
        self.setup_ui()
        
    def load_history(self):
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_history(self, path):
        if path in self.history:
            self.history.remove(path)
        self.history.insert(0, path)
        self.history = self.history[:5] # Keep only the last 5
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f)
            
        self.path_entry['values'] = self.history

    def setup_ui(self):
        lbl = tk.Label(self, text="Drop a folder, select a recent path, or paste below:", font=("Arial", 11))
        lbl.pack(pady=(20, 5))

        self.path_entry = ttk.Combobox(self, values=self.history, width=58, font=("Arial", 10))
        self.path_entry.pack(pady=5)
     
        self.path_entry.drop_target_register(DND_FILES)
        self.path_entry.dnd_bind('<<Drop>>', self.handle_drop)
        
        btn = tk.Button(self, text="Organize Folder", command=self.run_organizer, bg="#333", fg="white", font=("Arial", 10, "bold"))
        btn.pack(pady=15, ipadx=10, ipady=5)
        
        self.log_box = tk.Text(self, height=13, width=70, state='disabled', bg="#1e1e1e", fg="#4af626")
        self.log_box.pack(pady=10)
        
    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')
        self.update()

    def handle_drop(self, event):
        self.path_entry.delete(0, tk.END) 
        clean_path = event.data.strip('{}""\'')
        
        if clean_path.startswith("file://"):
            clean_path = clean_path.replace("file://", "")
            
        self.path_entry.insert(0, clean_path)

    def is_project_folder(self, target_dir):
        markers = ['.git', 'package.json', 'requirements.txt', 'pom.xml']
        for marker in markers:
            if (target_dir / marker).exists():
                return True
        return False

    def run_organizer(self):
        raw_path = self.path_entry.get().strip('\"\'')
        if not raw_path:
            messagebox.showwarning("Warning", "Please enter or drop a folder path first!")
            return
            
        p = Path(raw_path).expanduser().resolve()
        
        if not p.is_dir():
            self.log(f"Error: Could not find folder -> {p}")
            return
            
        if self.is_project_folder(p):
            confirm = messagebox.askyesno("Danger Zone", "This looks like a programming project (found .git or package files).\n\nAre you sure you want to reorganize it?")
            if not confirm:
                self.log("Aborted. Your codebase is safe.")
                return

        self.log(f"\n--- Sorting files in {p} ---")
        
        for item in p.iterdir():
            if item.is_dir() and item.suffix.lower() != '.app':
                continue
            if item.name.startswith('.'):
                continue
            if item.name in ['gui_organizer.py', 'gui_organizer']:
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
            
            final_dest = dest_path / item.name
            counter = 1
            while final_dest.exists():
                final_dest = dest_path / f"{item.stem}_{counter}{item.suffix}"
                counter += 1

            try:
                shutil.move(str(item), str(final_dest))
                self.log(f"Moved: {item.name} -> {dest_folder}/")
            except Exception as e:
                self.log(f"Couldn't move {item.name}: {e}")
                
        self.log("Done sorting!\n")

        self.save_history(str(p))
        
        self.path_entry.set("")

if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()