#!/usr/bin/env python3
"""
Validation script for abilities.json
"""

import json
import os

def main():
    # Path setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    abilities_file = os.path.join(project_root, 'data', 'core', 'abilities.json')
    
    print(f"Validating: {abilities_file}")
    
    # Load abilities
    with open(abilities_file, 'r') as f:
        abilities = json.load(f)
    
    # Expected abilities (in order)
    expected_abilities = [
        {"name": "strength", "title": "Strength", "short": "Str"},
        {"name": "dexterity", "title": "Dexterity", "short": "Dex"},
        {"name": "constitution", "title": "Constitution", "short": "Con"},
        {"name": "intelligence", "title": "Intelligence", "short": "Int"},
        {"name": "wisdom", "title": "Wisdom", "short": "Wis"},
        {"name": "charisma", "title": "Charisma", "short": "Cha"}
    ]
    
    issues = []
    
    # Check count
    if len(abilities) != 6:
        issues.append(f"Expected 6 abilities, found {len(abilities)}")
    
    # Check each ability
    for i, expected in enumerate(expected_abilities):
        if i >= len(abilities):
            issues.append(f"Missing ability: {expected['title']}")
            continue
            
        ability = abilities[i]
        
        # Check required fields
        required_fields = ['name', 'title', 'short', 'description', 'source', 'rules', 'type']
        for field in required_fields:
            if field not in ability:
                issues.append(f"{ability.get('title', f'Ability {i+1}')}: Missing field '{field}'")
            elif ability[field] == "":
                issues.append(f"{ability.get('title', f'Ability {i+1}')}: Empty field '{field}'")
        
        # Check specific values
        if 'name' in ability and ability['name'] != expected['name']:
            issues.append(f"Expected name '{expected['name']}', got '{ability['name']}'")
        
        if 'title' in ability and ability['title'] != expected['title']:
            issues.append(f"Expected title '{expected['title']}', got '{ability['title']}'")
        
        if 'short' in ability and ability['short'] != expected['short']:
            issues.append(f"Expected short '{expected['short']}', got '{ability['short']}'")
        
        # Check type and source
        if 'type' in ability and ability['type'] != 'abilities':
            issues.append(f"{ability['title']}: Expected type 'abilities', got '{ability['type']}'")
        
        if 'source' in ability and ability['source'] != 'SRD 5.2.1':
            issues.append(f"{ability['title']}: Expected source 'SRD 5.2.1', got '{ability['source']}'")
        
        # Check rules reference
        if 'rules' in ability:
            if not isinstance(ability['rules'], list) or len(ability['rules']) != 1 or ability['rules'][0] != 'abilityScore':
                issues.append(f"{ability['title']}: Expected rules ['abilityScore'], got {ability['rules']}")
    
    # Print results
    print(f"\n=== VALIDATION RESULTS ===")
    print(f"Total abilities: {len(abilities)}")
    
    if issues:
        print(f"\n❌ ISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"\n✅ No issues found")
    
    # Show abilities
    print(f"\n=== ABILITIES ===")
    for ability in abilities:
        print(f"  {ability.get('title', 'Unknown')} ({ability.get('short', '?')}) - {ability.get('description', 'No description')}")
    
    # Final status
    if len(issues) == 0:
        print(f"\n🎉 VALIDATION PASSED! All 6 abilities are properly defined.")
    else:
        print(f"\n⚠️  VALIDATION FAILED! Found {len(issues)} issues.")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)