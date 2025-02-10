def clean_cfg_file(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process lines to remove consecutive empty lines
    processed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()
    
        # Check if the current line is empty and the next line is also empty
        if stripped_line == '' and i + 1 < len(lines):
            # Skip this line if it and the next line are both empty
            i += 1
            continue
        processed_lines.append(line)
        i += 1

    # Write the processed lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(processed_lines)
        
        
def add_newline_after_third_line(file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Insert a newline after the third line
    if len(lines) >= 2:
        lines.insert(2, '\n')

    # Write the modified lines back to a new file
    with open(file_path, 'w') as file:
        file.writelines(lines)

        