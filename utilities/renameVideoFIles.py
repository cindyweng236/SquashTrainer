import os

def renameFiles(folderPath, category):
    for i, filename in enumerate(os.listdir(folderPath)):
        old_path = os.path.join(folderPath, filename)

        if os.path.isfile(old_path):
            _, ext = os.path.splitext(filename)
            new_filename = f"{category}_{i+1}{ext}"
            new_path = os.path.join(folderPath, new_filename)

            os.rename(old_path, new_path)

    print(f"Renaming {category} at {folderPath} complete!")