import os

def split_file(input_file, num_parts=4):
    """Split a file into multiple parts of roughly equal size."""
    # Read all lines from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    lines_per_part = total_lines // num_parts
    
    # Create the output files
    for i in range(num_parts):
        start_idx = i * lines_per_part
        # For the last part, include all remaining lines
        end_idx = (i + 1) * lines_per_part if i < num_parts - 1 else total_lines
        
        output_file = f"{os.path.splitext(input_file)[0]}{i+1}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(lines[start_idx:end_idx])
        
        print(f"Created {output_file} with {end_idx - start_idx} lines")

if __name__ == "__main__":
    # Assuming this script is run from the utils/downloads directory
    split_file("spotify_urls_merged.txt")
    print("Split complete!") 