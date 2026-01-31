import os
import re
import csv
from pathlib import Path

def simple_yaml_parse_field(content, field_name):
    """
    Extract a field value from YAML content using simple regex parsing.
    Fields are expected to be under bank_info: section.
    """
    # Try to find the field (with optional indentation)
    pattern = rf'^\s+{field_name}:\s*(.+)$'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        value = match.group(1).strip()
        # Remove quotes if present
        value = value.strip('"\'')
        # Remove any trailing comments
        if '#' in value:
            value = value.split('#')[0].strip()
        # If it's a multiline indicator, try to get the content
        if value in ['|-', '|', '>-', '>']:
            # This is a multiline field, parse it differently
            start_pos = match.end()
            remaining = content[start_pos:]
            lines = []
            
            # Get the indentation level of the field
            field_line = content[:match.start()].split('\n')[-1] + content[match.start():match.end()]
            field_indent = len(field_line) - len(field_line.lstrip())
            
            for line in remaining.split('\n'):
                if not line.strip():
                    continue
                # Stop if we hit another key at the same or lower indentation level
                if ':' in line:
                    line_indent = len(line) - len(line.lstrip())
                    if line_indent <= field_indent:
                        break
                # Collect indented content lines
                lines.append(line.strip())
            
            return ' '.join(lines)
        return value
    
    return None

def normalize_author_name(author):
    """
    Normalize author names by removing parenthetical content and extra whitespace.
    E.g., "Zhongzhou Chen (q1 - 10)" -> "Zhongzhou Chen"
    """
    # Remove anything in parentheses
    normalized = re.sub(r'\s*\([^)]*\)', '', author)
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    return normalized.strip()

def extract_first_author(content):
    """
    Extract the first author from the authors field.
    """
    # Look for "authors:" section
    authors_match = re.search(r'^\s+authors:\s*$', content, re.MULTILINE)
    if authors_match:
        # Found authors: on its own line, look for first list item
        start_pos = authors_match.end()
        remaining = content[start_pos:]
        
        for line in remaining.split('\n'):
            # Stop if we hit another key
            if line and not line[0].isspace() and ':' in line:
                break
            # Match first list item
            list_item = re.match(r'^\s*-\s*(.+)$', line)
            if list_item:
                author = list_item.group(1).strip()
                author = author.strip('"\'')
                return normalize_author_name(author)
    else:
        # Try inline format: authors: [...] or single value
        inline_match = re.search(r'^\s+authors:\s*\[(.+?)\]', content, re.MULTILINE)
        if inline_match:
            author_list = inline_match.group(1)
            first_author = author_list.split(',')[0].strip().strip('"\'')
            return normalize_author_name(first_author)
        else:
            # Try single value
            single_match = re.search(r'^\s+authors:\s*(.+)$', content, re.MULTILINE)
            if single_match:
                author = single_match.group(1).strip().strip('"\'')
                if not author.startswith('['):
                    return normalize_author_name(author)
    
    return ''

def count_questions(content):
    """
    Count the number of questions in the YAML file.
    """
    # Find the questions: section
    questions_match = re.search(r'^questions:\s*$', content, re.MULTILINE)
    if not questions_match:
        return 0
    
    start_pos = questions_match.end()
    remaining = content[start_pos:]
    
    # Count items that start with "- " followed by a problem type (e.g., "numerical:", "multiple_choice:")
    count = 0
    for line in remaining.split('\n'):
        # Match lines like "- numerical:" or "- multiple_choice:"
        if re.match(r'^-\s+\w+:\s*', line):
            count += 1
    
    return count

def get_first_problem_type(content):
    """
    Get the type of the first problem in the questions section.
    """
    # Find the questions: section
    questions_match = re.search(r'^questions:\s*$', content, re.MULTILINE)
    if not questions_match:
        return ''
    
    start_pos = questions_match.end()
    remaining = content[start_pos:]
    
    # Find the first problem type
    for line in remaining.split('\n'):
        # Match lines like "- numerical:" or "- multiple_choice:"
        match = re.match(r'^-\s+(\w+):\s*', line)
        if match:
            return match.group(1)
    
    return ''

def extract_bank_info(file_path):
    """Extract topic, bank_id, title, description, author, number of problems, and problem type from a YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract fields
        bank_id = simple_yaml_parse_field(content, 'bank_id')
        title = simple_yaml_parse_field(content, 'title')
        description = simple_yaml_parse_field(content, 'description')
        author = extract_first_author(content)
        num_problems = count_questions(content)
        problem_type = get_first_problem_type(content)
        
        # Get the topic (parent folder name, one level above the bank folder)
        # Structure: base_dir / topic_folder / bank_folder / bank_file.yaml
        topic = file_path.parent.parent.name
        
        return {
            'Topic': topic,
            'BankId': bank_id or '',
            'Title': title or '',
            'Description': description or '',
            'Author': author,
            'Number of problems': num_problems,
            'Problem Type': problem_type
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    # Base directory - go up one level from Bank Statistics to PHY I Mechanics
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent / "PHY I Mechanics"
    
    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        return
    
    # Find all .yaml and .yml files
    yaml_files = list(base_dir.glob("**/*.yaml")) + list(base_dir.glob("**/*.yml"))
    
    # Filter to only include files that:
    # 1. Are directly under a folder starting with "PHY1"
    # 2. The file itself starts with "PHY1"
    main_files = []
    
    for yaml_file in yaml_files:
        try:
            rel_path = yaml_file.relative_to(base_dir)
            parts = rel_path.parts
            
            # Check if file name starts with "PHY1"
            if not yaml_file.name.startswith("PHY1"):
                continue
            
            # Check if the file is directly under a folder starting with "PHY1"
            if len(parts) >= 2:
                parent_folder = parts[-2]
                if parent_folder.startswith("PHY1"):
                    main_files.append(yaml_file)
        except ValueError:
            continue
    
    print(f"Found {len(main_files)} valid problem bank files\n")
    
    # Extract information from each file
    bank_data = []
    for yaml_file in sorted(main_files):
        info = extract_bank_info(yaml_file)
        if info:
            bank_data.append(info)
    
    # Write to CSV
    output_file = script_dir / "problem_banks_table.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Topic', 'BankId', 'Title', 'Description', 'Author', 'Number of problems', 'Problem Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in bank_data:
            writer.writerow(row)
    
    print(f"✓ Created CSV table with {len(bank_data)} banks")
    print(f"✓ Output saved to: {output_file}")
    
    # Display preview
    print("\nPreview (first 5 rows):")
    print("-" * 80)
    for i, row in enumerate(bank_data[:5]):
        print(f"\n{i+1}. Topic: {row['Topic']}")
        print(f"   Bank ID: {row['BankId']}")
        print(f"   Title: {row['Title']}")
        print(f"   Author: {row['Author']}")
        print(f"   # Problems: {row['Number of problems']}")
        print(f"   Problem Type: {row['Problem Type']}")
        print(f"   Description: {row['Description'][:80]}..." if len(row['Description']) > 80 else f"   Description: {row['Description']}")

if __name__ == "__main__":
    main()
