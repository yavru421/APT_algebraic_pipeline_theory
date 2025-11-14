#!/usr/bin/env python3
"""
APT Module: m2_inventory_classifier
Algebraic Pipeline Theory - InventoryAI Classifier

Contract:
  Inputs:
    - scanned_items: list[dict] (output from m1_inventory_scanner)
    - classification_rules: dict (optional rules for classification)
  Outputs:
    - classified_items: list[dict] (items with category, priority, status)
  Errors:
    - ValueError if scanned_items is empty or invalid
  Success:
    - Returns items with classification metadata (category, priority, status)

Algebraic: y2 = m2(y1, x_rules)
"""

import sys
import os
import json
from datetime import datetime

# Import strict mode for fatal error handling
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import strict_mode

def classify_item(item: dict, rules: dict) -> dict:
    """
    Classify a single inventory item based on rules
    
    Default classification logic:
    - Category: Based on name patterns or explicit rules
    - Priority: Based on quantity thresholds
    - Status: Based on availability
    """
    raw_data = item.get('raw_data', {})
    
    # Extract common fields
    name = raw_data.get('name', 'Unknown')
    quantity = raw_data.get('quantity', 0)
    location = raw_data.get('location', 'Unknown')
    
    # Category classification
    category = rules.get('default_category', 'General')
    for pattern, cat in rules.get('category_patterns', {}).items():
        if pattern.lower() in name.lower():
            category = cat
            break
    
    # Priority classification based on quantity
    if quantity == 0:
        priority = 'CRITICAL'
        status = 'OUT_OF_STOCK'
    elif quantity < rules.get('low_stock_threshold', 20):
        priority = 'HIGH'
        status = 'LOW_STOCK'
    elif quantity < rules.get('medium_stock_threshold', 50):
        priority = 'MEDIUM'
        status = 'NORMAL'
    else:
        priority = 'LOW'
        status = 'IN_STOCK'
    
    # Create classified item
    classified = {
        'item_id': item.get('scan_id'),
        'classification_timestamp': datetime.now().isoformat(),
        'category': category,
        'priority': priority,
        'status': status,
        'metadata': {
            'name': name,
            'quantity': quantity,
            'location': location
        },
        'original_scan': item
    }
    
    return classified

def run(**kwargs) -> list[dict]:
    """
    Main entry point for m2_inventory_classifier module
    
    Args:
        scanned_items: List of scanned inventory items from m1
        classification_rules: Optional dict of classification rules
    
    Returns:
        List of classified inventory items
    """
    scanned_items = kwargs.get('scanned_items')
    classification_rules = kwargs.get('classification_rules', {})
    
    if not scanned_items:
        raise ValueError("⊥ scanned_items is required and cannot be empty")
    
    if not isinstance(scanned_items, list):
        raise ValueError("⊥ scanned_items must be a list")
    
    print(f"🏷️  APT m2_inventory_classifier")
    print(f"   Input: scanned_items count = {len(scanned_items)}")
    print(f"   Input: classification_rules = {bool(classification_rules)}")
    
    # Default classification rules
    default_rules = {
        'default_category': 'General',
        'category_patterns': {
            'widget': 'Electronics',
            'tool': 'Hardware',
            'part': 'Components',
            'material': 'RawMaterials'
        },
        'low_stock_threshold': 20,
        'medium_stock_threshold': 50
    }
    
    # Merge with provided rules
    rules = {**default_rules, **classification_rules}
    
    # Classify all items
    classified_items = []
    for item in scanned_items:
        classified = classify_item(item, rules)
        classified_items.append(classified)
    
    # Summary statistics
    categories = {}
    priorities = {}
    statuses = {}
    
    for item in classified_items:
        cat = item['category']
        pri = item['priority']
        stat = item['status']
        
        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1
        statuses[stat] = statuses.get(stat, 0) + 1
    
    print(f"   Output: classified_items count = {len(classified_items)}")
    print(f"   Categories: {categories}")
    print(f"   Priorities: {priorities}")
    print(f"   Statuses: {statuses}")
    print(f"✅ m2_inventory_classifier complete: y2 = m2(y1={len(scanned_items)} items)")
    
    return classified_items

if __name__ == "__main__":
    # Test module independently
    test_scanned_items = [
        {
            'scan_id': 'SCAN_001',
            'scan_timestamp': datetime.now().isoformat(),
            'raw_data': {'name': 'Widget A', 'quantity': 100, 'location': 'Warehouse A'}
        },
        {
            'scan_id': 'SCAN_002',
            'scan_timestamp': datetime.now().isoformat(),
            'raw_data': {'name': 'Tool B', 'quantity': 5, 'location': 'Warehouse B'}
        },
        {
            'scan_id': 'SCAN_003',
            'scan_timestamp': datetime.now().isoformat(),
            'raw_data': {'name': 'Part C', 'quantity': 0, 'location': 'Warehouse A'}
        }
    ]
    
    result = run(scanned_items=test_scanned_items)
    print(f"\nTest result: {len(result)} items classified")
    print(json.dumps(result[0], indent=2))
