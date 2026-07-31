import os
import re

def clean_gutenberg_file(filepath):
    """
    Reads a text file, strips Gutenberg markers, and overwrites the file 
    with the clean text. Handles variations in Gutenberg spacing.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # The \s* allows the script to catch the marker whether there is a space or not
    start_pattern = r'\*\*\*\s*START OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    end_pattern = r'\*\*\*\s*END OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'

    start_match = re.search(start_pattern, text)
    end_match = re.search(end_pattern, text)

    if start_match and end_match:
        # Extract the actual book text
        clean_text = text[start_match.end():end_match.start()].strip()
        
        # Overwrite the original file with the clean version
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_text)
            
        print(f"SUCCESS: Cleaned '{filepath}'")
    else:
        print(f"SKIPPED: No Gutenberg markers found in '{filepath}'")

if __name__ == "__main__":
    # Point to the root of the training data folder
    students_dir = os.path.join("data", "students")
    
    print("Starting batch cleanup of training data...\n")
    
    # Loop through A, B, C, D, E folders
    if os.path.exists(students_dir):
        for author_folder in os.listdir(students_dir):
            folder_path = os.path.join(students_dir, author_folder)
            
            # Ensure it's a directory
            if os.path.isdir(folder_path):
                # Process every .txt file in this author's folder
                for filename in os.listdir(folder_path):
                    if filename.endswith(".txt"):
                        filepath = os.path.join(folder_path, filename)
                        clean_gutenberg_file(filepath)
                        
        print("\nAll training data cleaned successfully!")
    else:
        print(f"Error: Could not find the directory '{students_dir}'")
