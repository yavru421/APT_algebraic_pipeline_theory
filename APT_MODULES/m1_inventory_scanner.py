#!/usr/bin/env python3
"""
APT Module: m1_inventory_scanner
Algebraic Pipeline Theory - InventoryAI Scanner

Contract:
  Inputs: 
    - inventory_path: str (path to inventory data source)
    - scan_type: str (type of scan: 'file', 'directory', 'database')
  Outputs:
    - scanned_items: list[dict] (raw inventory items with metadata)
  Errors:
    - FileNotFoundError if path doesn't exist
    - ValueError if scan_type is invalid
  Success:
    - Returns list of scanned items with id, name, location, timestamp

Algebraic: y1 = m1(x_path, x_scan_type)
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Import strict mode for fatal error handling
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import strict_mode

def scan_file_inventory(file_path: str) -> list[dict]:
    """Scan a JSON file containing inventory data"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"⊥ Inventory file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and 'items' in data:
        items = data['items']
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"⊥ Invalid inventory file format. Expected list or dict with 'items' key")
    
    # Enrich with metadata
    scanned_items = []
    for idx, item in enumerate(items):
        enriched_item = {
            'scan_id': f"SCAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}",
            'scan_timestamp': datetime.now().isoformat(),
            'raw_data': item
        }
        scanned_items.append(enriched_item)
    
    return scanned_items

def scan_directory_inventory(dir_path: str) -> list[dict]:
    """Scan a directory for inventory items (files)"""
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"⊥ Inventory directory not found: {dir_path}")
    
    if not os.path.isdir(dir_path):
        raise ValueError(f"⊥ Path is not a directory: {dir_path}")
    
    scanned_items = []
    for idx, file_path in enumerate(Path(dir_path).rglob('*')):
        if file_path.is_file():
            item = {
                'scan_id': f"SCAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}",
                'scan_timestamp': datetime.now().isoformat(),
                'raw_data': {
                    'name': file_path.name,
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
            }
            scanned_items.append(item)
    
    return scanned_items

def run(**kwargs) -> list[dict]:
    """
    Main entry point for m1_inventory_scanner module
    
    Args:
        inventory_path: Path to inventory source
        scan_type: Type of scan ('file' or 'directory')
    
    Returns:
        List of scanned inventory items
    """
    inventory_path = kwargs.get('inventory_path')
    scan_type = kwargs.get('scan_type', 'file')
    
    if not inventory_path:
        raise ValueError("⊥ inventory_path is required")
    
    print(f"📊 APT m1_inventory_scanner")
    print(f"   Input: inventory_path = {inventory_path}")
    print(f"   Input: scan_type = {scan_type}")
    
    if scan_type == 'file':
        scanned_items = scan_file_inventory(inventory_path)
    elif scan_type == 'directory':
        scanned_items = scan_directory_inventory(inventory_path)
    else:
        raise ValueError(f"⊥ Invalid scan_type: {scan_type}. Must be 'file' or 'directory'")
    
    print(f"   Output: scanned_items count = {len(scanned_items)}")
    print(f"✅ m1_inventory_scanner complete: y1 = m1(x_path={inventory_path}, x_scan_type={scan_type})")
    
    return scanned_items

if __name__ == "__main__":
    # Test module independently
    test_data = {
        "items": [
            {"id": 1, "name": "Widget A", "quantity": 100, "location": "Warehouse A"},
            {"id": 2, "name": "Widget B", "quantity": 50, "location": "Warehouse B"},
            {"id": 3, "name": "Widget C", "quantity": 75, "location": "Warehouse A"}
        ]
    }
    
    # Create test file
    test_file = "/tmp/test_inventory.json"
    with open(test_file, 'w') as f:
        json.dump(test_data, f)
    
    result = run(inventory_path=test_file, scan_type='file')
    print(f"\nTest result: {len(result)} items scanned")
    print(json.dumps(result[0], indent=2))
