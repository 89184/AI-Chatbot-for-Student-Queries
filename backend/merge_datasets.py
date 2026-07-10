import json
import os
import random

print("=" * 60)
print(" MERGING DATASETS")
print("=" * 60)

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" File not found: {filepath}")
        return None

def save_json(data, filepath):
    """Save JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f" Saved to {filepath}")

def convert_to_intents(data):
    """Convert dataset to intents.json format"""
    intents = {"intents": []}
    
    # Group by category or tag
    categories = {}
    for item in data:
        cat = item.get('category', 'general')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # Create intents for each category
    for category, items in categories.items():
        patterns = []
        responses = []
        for item in items[:20]:  # Limit per category to avoid overfitting
            if item.get('instruction'):
                patterns.append(item['instruction'])
            if item.get('response'):
                responses.append(item['response'])
        
        if patterns and responses:
            intents["intents"].append({
                "tag": category,
                "patterns": patterns,
                "responses": responses
            })
    
    return intents

def merge_datasets():
    """Merge original and IEEE datasets"""
    
    # Load original intents
    original = load_json('data/intents.json')
    if original:
        print(f" Original intents: {len(original.get('intents', []))} intents")
    
    # Load IEEE dataset
    ieee = load_json('data/ieee_dataset.json')
    
    combined = {"intents": []}
    
    # Add original intents
    if original and 'intents' in original:
        combined['intents'].extend(original['intents'])
    
    # Convert IEEE dataset to intents format
    if ieee:
        ieee_intents = convert_to_intents(ieee)
        if ieee_intents and 'intents' in ieee_intents:
            combined['intents'].extend(ieee_intents['intents'])
    
    # Remove duplicates based on tag
    seen_tags = set()
    unique_intents = []
    for intent in combined['intents']:
        tag = intent.get('tag', 'unknown')
        if tag not in seen_tags:
            seen_tags.add(tag)
            unique_intents.append(intent)
        else:
            # Merge patterns and responses
            for existing in unique_intents:
                if existing['tag'] == tag:
                    existing['patterns'].extend(intent['patterns'])
                    existing['responses'].extend(intent['responses'])
                    break
    
    combined['intents'] = unique_intents
    
    print(f"\n Combined Dataset:")
    print(f"   - Total Intents: {len(combined['intents'])}")
    total_patterns = sum(len(i['patterns']) for i in combined['intents'])
    total_responses = sum(len(i['responses']) for i in combined['intents'])
    print(f"   - Total Patterns: {total_patterns}")
    print(f"   - Total Responses: {total_responses}")
    
    # Save combined dataset
    save_json(combined, 'data/combined_intents.json')
    
    # Also update the main intents.json (backup original)
    if original:
        save_json(original, 'data/intents_backup.json')
    
    # Replace main intents with combined
    save_json(combined, 'data/intents.json')
    
    print("\n" + "=" * 60)
    print(" DATASET MERGING COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    merge_datasets()