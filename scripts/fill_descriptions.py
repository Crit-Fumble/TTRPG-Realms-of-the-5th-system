#!/usr/bin/env python3
"""
Script to fill remaining empty descriptions in rules.json from SRD content
"""

import json
import re
import os

def find_srd_content(title, srd_content):
    """Find the SRD content for a given rule title"""
    # Try to find the exact header match
    pattern = f"#### {re.escape(title)}"
    match = re.search(pattern, srd_content, re.MULTILINE)
    
    if match:
        start = match.end()
        # Find the next #### to get the content
        next_header = re.search(r'\n#### ', srd_content[start:])
        if next_header:
            end = start + next_header.start()
        else:
            end = len(srd_content)
        
        content = srd_content[start:end].strip()
        # Get the first paragraph as description
        lines = content.split('\n')
        description_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                break
            if line.startswith('*See also*') or line.startswith('Table:') or line.startswith('|'):
                break
            if line.startswith('**') and line.endswith('**'):
                break
            description_lines.append(line)
        
        description = ' '.join(description_lines).strip()
        # Clean up markdown artifacts
        description = re.sub(r'\*([^*]+)\*', r'\1', description)  # Remove italic markers
        description = re.sub(r'\s+', ' ', description)  # Normalize whitespace
        
        return description
    
    return None

def main():
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    rules_file = os.path.join(project_root, 'data', 'core', 'rules.json')
    srd_file = os.path.join(project_root, 'srd', 'srd-5.2.1-cc.md')
    
    # Load files
    with open(rules_file, 'r') as f:
        rules = json.load(f)
    
    with open(srd_file, 'r') as f:
        srd_content = f.read()
    
    # Find empty descriptions
    updated_count = 0
    for rule in rules:
        if rule.get('description') == "":
            title = rule['title']
            description = find_srd_content(title, srd_content)
            
            if description:
                rule['description'] = description
                rule['source'] = 'SRD 5.2.1'
                updated_count += 1
                print(f"Updated '{title}': {description[:60]}...")
            else:
                print(f"No content found for '{title}'")
    
    # Save updated rules
    with open(rules_file, 'w') as f:
        json.dump(rules, f, indent=4)
    
    print(f"\nUpdated {updated_count} rules")

if __name__ == "__main__":
    main()