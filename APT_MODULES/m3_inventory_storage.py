#!/usr/bin/env python3
"""
APT Module: m3_inventory_storage
Algebraic Pipeline Theory - InventoryAI Storage

Contract:
  Inputs:
    - classified_items: list[dict] (output from m2_inventory_classifier)
    - storage_path: str (path to store inventory data)
    - storage_format: str (format: 'json', 'csv')
  Outputs:
    - storage_result: dict (storage metadata and path)
  Errors:
    - ValueError if classified_items is empty
    - IOError if storage fails
  Success:
    - Data stored successfully with timestamp and checksum

Algebraic: y3 = m3(y2, x_path, x_format)
"""

import sys
import os
import json
import csv
import hashlib
from datetime import datetime
from pathlib import Path

# Import strict mode for fatal error handling
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import strict_mode

def compute_checksum(data: str) -> str:
    """Compute SHA256 checksum of data"""
    return hashlib.sha256(data.encode()).hexdigest()

def store_as_json(items: list[dict], file_path: str) -> dict:
    """Store inventory items as JSON"""
    storage_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'item_count': len(items),
            'format': 'json',
            'version': '1.0'
        },
        'items': items
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write file
    json_str = json.dumps(storage_data, indent=2)
    with open(file_path, 'w') as f:
        f.write(json_str)
    
    checksum = compute_checksum(json_str)
    file_size = os.path.getsize(file_path)
    
    return {
        'path': file_path,
        'format': 'json',
        'size_bytes': file_size,
        'checksum': checksum
    }

def store_as_csv(items: list[dict], file_path: str) -> dict:
    """Store inventory items as CSV"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Flatten items for CSV
    flattened_items = []
    for item in items:
        flat = {
            'item_id': item.get('item_id'),
            'classification_timestamp': item.get('classification_timestamp'),
            'category': item.get('category'),
            'priority': item.get('priority'),
            'status': item.get('status'),
            'name': item.get('metadata', {}).get('name'),
            'quantity': item.get('metadata', {}).get('quantity'),
            'location': item.get('metadata', {}).get('location')
        }
        flattened_items.append(flat)
    
    # Write CSV
    if flattened_items:
        fieldnames = list(flattened_items[0].keys())
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_items)
    
    # Compute checksum
    with open(file_path, 'r') as f:
        csv_content = f.read()
    
    checksum = compute_checksum(csv_content)
    file_size = os.path.getsize(file_path)
    
    return {
        'path': file_path,
        'format': 'csv',
        'size_bytes': file_size,
        'checksum': checksum
    }

def run(**kwargs) -> dict:
    """
    Main entry point for m3_inventory_storage module
    
    Args:
        classified_items: List of classified inventory items from m2
        storage_path: Path where to store the data
        storage_format: Format for storage ('json' or 'csv')
    
    Returns:
        Dictionary with storage metadata
    """
    classified_items = kwargs.get('classified_items')
    storage_path = kwargs.get('storage_path')
    storage_format = kwargs.get('storage_format', 'json')
    
    if not classified_items:
        raise ValueError("⊥ classified_items is required and cannot be empty")
    
    if not storage_path:
        raise ValueError("⊥ storage_path is required")
    
    print(f"💾 APT m3_inventory_storage")
    print(f"   Input: classified_items count = {len(classified_items)}")
    print(f"   Input: storage_path = {storage_path}")
    print(f"   Input: storage_format = {storage_format}")
    
    # Store based on format
    if storage_format == 'json':
        storage_result = store_as_json(classified_items, storage_path)
    elif storage_format == 'csv':
        storage_result = store_as_csv(classified_items, storage_path)
    else:
        raise ValueError(f"⊥ Invalid storage_format: {storage_format}. Must be 'json' or 'csv'")
    
    # Add timestamp
    storage_result['storage_timestamp'] = datetime.now().isoformat()
    storage_result['item_count'] = len(classified_items)
    
    print(f"   Output: storage_result = {storage_result['path']}")
    print(f"   Size: {storage_result['size_bytes']} bytes")
    print(f"   Checksum: {storage_result['checksum'][:16]}...")
    print(f"✅ m3_inventory_storage complete: y3 = m3(y2={len(classified_items)} items, path={storage_path})")
    
    return storage_result

if __name__ == "__main__":
    # Test module independently
    from datetime import datetime
    
    test_classified_items = [
        {
            'item_id': 'SCAN_001',
            'classification_timestamp': datetime.now().isoformat(),
            'category': 'Electronics',
            'priority': 'LOW',
            'status': 'IN_STOCK',
            'metadata': {'name': 'Widget A', 'quantity': 100, 'location': 'Warehouse A'}
        },
        {
            'item_id': 'SCAN_002',
            'classification_timestamp': datetime.now().isoformat(),
            'category': 'Hardware',
            'priority': 'HIGH',
            'status': 'LOW_STOCK',
            'metadata': {'name': 'Tool B', 'quantity': 5, 'location': 'Warehouse B'}
        }
    ]
    
    # Test JSON storage
    result_json = run(
        classified_items=test_classified_items,
        storage_path='/tmp/inventory_output.json',
        storage_format='json'
    )
    print(f"\nJSON Test result: {result_json}")
    
    # Test CSV storage
    result_csv = run(
        classified_items=test_classified_items,
        storage_path='/tmp/inventory_output.csv',
        storage_format='csv'
    )
    print(f"\nCSV Test result: {result_csv}")
