import os

def list_files_and_folders(root_dir, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = []

    for root, dirs, files in os.walk(root_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    ignore_dirs = ['__pycache__', 'media', '.git']
    print(f"Listing files and folders in: {current_directory}\n")
    list_files_and_folders(current_directory, ignore_dirs)
