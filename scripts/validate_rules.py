#!/usr/bin/env python3
"""
Validation script to verify the rules.json transformation is complete and correct
"""

import json
import os

def main():
    # Path setup
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    rules_file = os.path.join(project_root, 'data', 'core', 'rules.json')
    
    print(f"Validating: {rules_file}")
    
    # Load rules
    with open(rules_file, 'r') as f:
        rules = json.load(f)
    
    # Create name mapping for validation
    names = set()
    titles = set()
    
    # Check each rule
    issues = []
    for i, rule in enumerate(rules):
        rule_id = f"Rule {i+1}"
        
        # Check required fields
        if 'name' not in rule:
            issues.append(f"{rule_id}: Missing 'name' field")
        if 'title' not in rule:
            issues.append(f"{rule_id}: Missing 'title' field")
        
        if 'name' in rule:
            if rule['name'] in names:
                issues.append(f"{rule_id}: Duplicate name '{rule['name']}'")
            names.add(rule['name'])
        
        if 'title' in rule:
            if rule['title'] in titles:
                issues.append(f"{rule_id}: Duplicate title '{rule['title']}'")
            titles.add(rule['title'])
    
    # Create lookup for reference validation
    name_to_title = {rule['name']: rule['title'] for rule in rules if 'name' in rule}
    
    # Check references
    reference_issues = []
    for rule in rules:
        if 'super' in rule and rule['super']:
            for ref in rule['super']:
                if ref not in names:
                    reference_issues.append(f"'{rule['title']}' has invalid super reference '{ref}'")
        
        if 'sub' in rule and rule['sub']:
            for ref in rule['sub']:
                if ref not in names:
                    reference_issues.append(f"'{rule['title']}' has invalid sub reference '{ref}'")
    
    # Print results
    print(f"\n=== VALIDATION RESULTS ===")
    print(f"Total rules: {len(rules)}")
    print(f"Rules with names: {len(names)}")
    print(f"Unique titles: {len(titles)}")
    
    if issues:
        print(f"\n❌ STRUCTURAL ISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"\n✅ No structural issues found")
    
    if reference_issues:
        print(f"\n❌ REFERENCE ISSUES ({len(reference_issues)}):")
        for issue in reference_issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(reference_issues) > 10:
            print(f"  ... and {len(reference_issues) - 10} more")
    else:
        print(f"\n✅ All references are valid")
    
    # Show sample transformations
    print(f"\n=== SAMPLE TRANSFORMATIONS ===")
    for i, rule in enumerate(rules[:5]):
        refs = []
        if 'super' in rule and rule['super']:
            refs.append(f"super: {rule['super']}")
        if 'sub' in rule and rule['sub']:
            refs.append(f"sub: {rule['sub']}")
        ref_str = f" ({', '.join(refs)})" if refs else ""
        print(f"  '{rule['title']}' → '{rule['name']}'{ref_str}")
    
    # Final status
    total_issues = len(issues) + len(reference_issues)
    if total_issues == 0:
        print(f"\n🎉 VALIDATION PASSED! All {len(rules)} rules are properly transformed.")
    else:
        print(f"\n⚠️  VALIDATION FAILED! Found {total_issues} issues.")
    
    return total_issues == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)