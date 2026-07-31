import os
import re

def process_outsider_gutenberg(input_filepath, output_dir, chunk_size=350, max_cases=50):
    print(f"Reading {input_filepath}...")
    
    with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()

    # 1. Strip Gutenberg Headers (handles optional spaces)
    start_pattern = r'\*\*\*\s*START OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    end_pattern = r'\*\*\*\s*END OF TH(?:E|IS) PROJECT GUTENBERG EBOOK.*?\*\*\*'

    start_match = re.search(start_pattern, text)
    end_match = re.search(end_pattern, text)

    if start_match and end_match:
        # Extract only the actual document text
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
        
        # Only save full-sized chunks
        if len(chunk_words) == chunk_size:
            chunk_count += 1
            chunk_text = ' '.join(chunk_words)
            
            output_filename = os.path.join(output_dir, f"outsider_test_{chunk_count}.txt")
            with open(output_filename, 'w', encoding='utf-8') as out_file:
                out_file.write(chunk_text)
                
            # Stop once we hit the required number of test cases
            if chunk_count >= max_cases:
                break

    print(f"Success! Created {chunk_count} test cases for OUTSIDER in '{output_dir}'.")

if __name__ == "__main__":
    # Setup paths
    author_folder = "Outsider"
    input_file = os.path.join("data", "eval", author_folder, "outsider_raw.txt")
    output_directory = os.path.join("data", "eval", author_folder)
    
    # Run the processor
    if os.path.exists(input_file):
        process_outsider_gutenberg(input_file, output_directory, chunk_size=350, max_cases=50)
        
        print("\n--- CRITICAL NEXT STEP ---")
        print(f"Please DELETE or MOVE the original '{input_file}' file now!")
        print("If you leave it in the folder, the evaluation script will treat it as a giant 51st test case.")
    else:
        print(f"Error: Could not find '{input_file}'.")
        print("Please make sure you downloaded the text and saved it as 'outsider_raw.txt' in 'data/eval/Outsider/'")
