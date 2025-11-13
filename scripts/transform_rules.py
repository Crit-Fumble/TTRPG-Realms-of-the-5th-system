#!/usr/bin/env python3
"""
Script to transform rules.json by:
1. Adding camelCase "name" attribute to each rule
2. Converting "super" and "sub" references from titles to names
3. Handling the specific transformations already done
"""

import json
import re
import os

def title_to_camel_case(title):
    """Convert title to camelCase name"""
    # Handle special cases first
    special_cases = {
        "D20 Test": "d20Test",
        "AC": "ac",
        "CR": "cr",
        "AoE": "aoe"
    }
    
    if title in special_cases:
        return special_cases[title]
    
    # Remove special characters and split into words
    words = re.sub(r'[^\w\s]', '', title).split()
    
    # First word lowercase, subsequent words capitalized
    if not words:
        return ""
    
    camel_case = words[0].lower()
    for word in words[1:]:
        camel_case += word.capitalize()
    
    return camel_case

def load_rules(file_path):
    """Load the rules.json file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_rules(rules, file_path):
    """Save the rules.json file with proper formatting"""
    with open(file_path, 'w') as f:
        json.dump(rules, f, indent=4)

def main():
    # Determine the correct path to the rules file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    rules_file = os.path.join(project_root, 'data', 'core', 'rules.json')
    
    print(f"Loading rules from: {rules_file}")
    
    # Load rules
    rules = load_rules(rules_file)
    
    # First pass: Create mapping from title to name and add names
    title_to_name = {}
    
    print("Pass 1: Adding names to rules...")
    for i, rule in enumerate(rules):
        if 'name' not in rule:
            name = title_to_camel_case(rule['title'])
            # Reorder fields: name first, then title, then rest
            new_rule = {'name': name, 'title': rule['title']}
            for key, value in rule.items():
                if key not in ['name', 'title']:
                    new_rule[key] = value
            rules[i] = new_rule
        title_to_name[rule['title']] = rules[i]['name']
    
    print(f"Generated names for {len(title_to_name)} rules")
    
    # Second pass: Convert super/sub references from titles to names
    print("Pass 2: Converting references...")
    updated_count = 0
    for rule in rules:
        changed = False
        
        # Convert super references
        if 'super' in rule and rule['super']:
            new_super = []
            for super_ref in rule['super']:
                if super_ref in title_to_name:
                    new_super.append(title_to_name[super_ref])
                    changed = True
                elif any(title for title in title_to_name.keys() if title_to_name[title] == super_ref):
                    # Already converted to name
                    new_super.append(super_ref)
                else:
                    print(f"WARNING: Super reference '{super_ref}' not found for '{rule['title']}'")
                    new_super.append(super_ref)
            rule['super'] = new_super
        
        # Convert sub references  
        if 'sub' in rule and rule['sub']:
            new_sub = []
            for sub_ref in rule['sub']:
                if sub_ref in title_to_name:
                    new_sub.append(title_to_name[sub_ref])
                    changed = True
                elif any(title for title in title_to_name.keys() if title_to_name[title] == sub_ref):
                    # Already converted to name
                    new_sub.append(sub_ref)
                else:
                    print(f"WARNING: Sub reference '{sub_ref}' not found for '{rule['title']}'")
                    new_sub.append(sub_ref)
            rule['sub'] = new_sub
            
        if changed:
            updated_count += 1
    
    # Save transformed rules
    save_rules(rules, rules_file)
    print(f"Transformation complete! Updated {updated_count} rules with reference conversions.")
    
    # Print some examples
    print("\nSample transformations:")
    for i, rule in enumerate(rules[:5]):
        refs = []
        if 'super' in rule and rule['super']:
            refs.append(f"super: {rule['super']}")
        if 'sub' in rule and rule['sub']:
            refs.append(f"sub: {rule['sub']}")
        ref_str = f" ({', '.join(refs)})" if refs else ""
        print(f"  '{rule['title']}' -> name: '{rule['name']}'{ref_str}")
    
    # Final validation
    print(f"\nFinal stats:")
    print(f"Total rules: {len(rules)}")
    rules_with_names = sum(1 for rule in rules if 'name' in rule)
    print(f"Rules with names: {rules_with_names}")
    print(f"Rules without names: {len(rules) - rules_with_names}")

if __name__ == "__main__":
    main()