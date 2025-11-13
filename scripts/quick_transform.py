#!/usr/bin/env python3
"""
Quick transformation script to handle the rules.json conversion
Optimized for the current state of the file
"""

import json
import os

def to_camel_case(title):
    """Convert title to camelCase name"""
    # Handle special D20 case
    if "D20" in title:
        title = title.replace("D20", "d20")
    
    # Split and convert
    words = title.replace("-", " ").replace("(", "").replace(")", "").split()
    if not words:
        return ""
    
    result = words[0].lower()
    for word in words[1:]:
        result += word.capitalize()
    
    return result

def main():
    # Path setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    rules_file = os.path.join(project_root, 'data', 'core', 'rules.json')
    
    print(f"Processing: {rules_file}")
    
    # Load rules
    with open(rules_file, 'r') as f:
        rules = json.load(f)
    
    # Create title to name mapping
    title_to_name = {}
    
    # Add names to rules that don't have them
    for i, rule in enumerate(rules):
        if 'name' not in rule:
            name = to_camel_case(rule['title'])
            # Reorder to put name first
            new_rule = {'name': name}
            for key, value in rule.items():
                new_rule[key] = value
            rules[i] = new_rule
        
        title_to_name[rule['title']] = rules[i]['name']
    
    # Convert all super/sub references
    for rule in rules:
        if 'super' in rule and rule['super']:
            new_super = []
            for ref in rule['super']:
                if ref in title_to_name:
                    new_super.append(title_to_name[ref])
                else:
                    # Check if it's already a name
                    found = False
                    for title, name in title_to_name.items():
                        if name == ref:
                            new_super.append(ref)
                            found = True
                            break
                    if not found:
                        print(f"Warning: Unresolved super reference '{ref}' in '{rule['title']}'")
                        new_super.append(ref)
            rule['super'] = new_super
        
        if 'sub' in rule and rule['sub']:
            new_sub = []
            for ref in rule['sub']:
                if ref in title_to_name:
                    new_sub.append(title_to_name[ref])
                else:
                    # Check if it's already a name
                    found = False
                    for title, name in title_to_name.items():
                        if name == ref:
                            new_sub.append(ref)
                            found = True
                            break
                    if not found:
                        print(f"Warning: Unresolved sub reference '{ref}' in '{rule['title']}'")
                        new_sub.append(ref)
            rule['sub'] = new_sub
    
    # Save result
    with open(rules_file, 'w') as f:
        json.dump(rules, f, indent=4)
    
    print(f"Transformation completed!")
    print(f"Processed {len(rules)} rules")
    
    # Show summary
    names_added = sum(1 for rule in rules if 'name' in rule)
    print(f"Rules with names: {names_added}/{len(rules)}")

if __name__ == "__main__":
    main()