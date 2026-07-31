import os
import re

def process_gutenberg_book(input_filepath, output_dir, author_prefix, chunk_size=350):
    """
    Strips Gutenberg headers/footers and splits the text into chunks.
    """
    print(f"Reading {input_filepath}...")
    
    # Using errors='ignore' ensures weird character encodings don't crash the script
    with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()

    # 1. Find the start and end of the actual book content
    start_pattern = r'\*\*\* START OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    end_pattern = r'\*\*\* END OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'

    start_match = re.search(start_pattern, text)
    end_match = re.search(end_pattern, text)

    if start_match and end_match:
        # Extract only the text between the markers
        clean_text = text[start_match.end():end_match.start()]
    else:
        print(f"Warning: Standard Gutenberg markers not found in {input_filepath}. Processing entire file.")
        clean_text = text

    # 2. Clean up whitespace and line breaks
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    # 3. Split into words and create chunks
    words = clean_text.split()
    
    os.makedirs(output_dir, exist_ok=True)
    
    chunk_count = 0
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i + chunk_size]
        
        if len(chunk_words) == chunk_size:
            chunk_count += 1
            chunk_text = ' '.join(chunk_words)
            
            output_filename = os.path.join(output_dir, f"{author_prefix}_test_{chunk_count}.txt")
            with open(output_filename, 'w', encoding='utf-8') as out_file:
                out_file.write(chunk_text)
                
            if chunk_count >= 50:
                break

    print(f"Success! Created {chunk_count} test cases for {author_prefix.upper()} in '{output_dir}'.")

if __name__ == "__main__":
    # --- PROCESSING FOR OUTSIDER ---
    AUTHOR_FOLDER = "Outsider"
    FILE_PREFIX = "outsider"
    
    # Example: Make sure you saved the downloaded book as 'outsider_raw.txt' in the Outsider folder
    input_file = os.path.join("data", "eval", AUTHOR_FOLDER, "outsider_raw.txt")
    output_directory = os.path.join("data", "eval", AUTHOR_FOLDER)
    
    # Run the processor
    process_gutenberg_book(input_file, output_directory, FILE_PREFIX, chunk_size=350)
    
    print("\n--- REMINDER ---")
    print(f"Delete or move the original '{input_file}' before running evaluate_cipherink.py!")
