import os
import re
from collections import defaultdict
from pathlib import Path

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

def simple_yaml_parse_authors(file_path):
    """
    Extract authors from a YAML file using simple regex parsing.
    This avoids the need for PyYAML dependency.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for "authors:" section
        # Pattern: authors: followed by either a list or single value
        authors = []
        
        # First try to find "authors:" as a key
        authors_match = re.search(r'^authors:\s*$', content, re.MULTILINE)
        if authors_match:
            # Found authors: on its own line, look for list items after it
            start_pos = authors_match.end()
            remaining = content[start_pos:]
            
            # Extract list items (lines starting with - )
            for line in remaining.split('\n'):
                # Stop if we hit another top-level key (no indentation)
                if line and not line[0].isspace() and ':' in line:
                    break
                    
                # Match list items
                list_item = re.match(r'^\s*-\s*(.+)$', line)
                if list_item:
                    author = list_item.group(1).strip()
                    # Remove quotes if present
                    author = author.strip('"\'')
                    if author:
                        authors.append(normalize_author_name(author))
        else:
            # Try inline format: authors: [...]
            inline_match = re.search(r'authors:\s*\[(.*?)\]', content, re.DOTALL)
            if inline_match:
                author_list = inline_match.group(1)
                for author in re.split(r',', author_list):
                    author = author.strip().strip('"\'')
                    if author:
                        authors.append(normalize_author_name(author))
            else:
                # Try single value: authors: Name
                single_match = re.search(r'authors:\s*(.+)$', content, re.MULTILINE)
                if single_match:
                    author = single_match.group(1).strip().strip('"\'')
                    if author and not author.startswith('['):
                        authors.append(normalize_author_name(author))
        
        return authors
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    # Base directory - go up one level from Bank Statistics to PHY I Mechanics
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent / "PHY I Mechanics"
    
    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        return
    
    # Dictionary to store author counts and which files they authored
    author_counts = defaultdict(int)
    author_files = defaultdict(list)
    
    # Find all .yaml and .yml files
    yaml_files = list(base_dir.glob("**/*.yaml")) + list(base_dir.glob("**/*.yml"))
    
    # Filter to only include files that:
    # 1. Are directly under a folder starting with "PHY1"
    # 2. The file itself starts with "PHY1"
    main_files = []
    
    for yaml_file in yaml_files:
        # Get relative path from base_dir
        try:
            rel_path = yaml_file.relative_to(base_dir)
            parts = rel_path.parts
            
            # Check if file name starts with "PHY1"
            if not yaml_file.name.startswith("PHY1"):
                continue
            
            # Check if the file is directly under a folder starting with "PHY1"
            # The structure should be: topic_folder / PHY1-xxx / PHY1-xxx.yaml
            # So we need at least 2 parts (folder and file), and the parent folder should start with PHY1
            if len(parts) >= 2:
                parent_folder = parts[-2]  # The immediate parent folder
                if parent_folder.startswith("PHY1"):
                    main_files.append(yaml_file)
        except ValueError:
            continue
    
    print(f"Found {len(main_files)} main problem bank files\n")
    
    # Process each file
    for yaml_file in sorted(main_files):
        authors = simple_yaml_parse_authors(yaml_file)
        if authors:
            file_name = yaml_file.name
            for author in authors:
                if author:  # Skip empty strings
                    author_counts[author] += 1
                    author_files[author].append(file_name)
    
    # Display results
    print("=" * 80)
    print("AUTHOR TALLY - Problem Banks Authored")
    print("=" * 80)
    print()
    
    # Sort by count (descending), then by name
    sorted_authors = sorted(author_counts.items(), key=lambda x: (-x[1], x[0]))
    
    for author, count in sorted_authors:
        print(f"{author}: {count} problem bank(s)")
    
    print()
    print("=" * 80)
    print(f"Total unique authors: {len(author_counts)}")
    print(f"Total problem banks processed: {len(main_files)}")
    print("=" * 80)
    
    # Optional: Show detailed breakdown
    print("\nDetailed breakdown:")
    print("=" * 80)
    for author, count in sorted_authors:
        print(f"\n{author} ({count} banks):")
        for file in author_files[author]:
            print(f"  - {file}")

if __name__ == "__main__":
    main()
