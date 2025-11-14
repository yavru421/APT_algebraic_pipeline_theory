#!/usr/bin/env python3
"""
APT Module: m4_inventory_reporter
Algebraic Pipeline Theory - InventoryAI Reporter

Contract:
  Inputs:
    - storage_result: dict (output from m3_inventory_storage)
    - classified_items: list[dict] (for generating summary)
    - report_format: str ('summary', 'detailed', 'alerts')
  Outputs:
    - report: dict (final inventory report with insights and recommendations)
  Errors:
    - ValueError if storage_result or classified_items is invalid
  Success:
    - Returns comprehensive report with analytics and recommendations

Algebraic: Y = m4(y3, y2, x_report_format)
"""

import sys
import os
import json
from datetime import datetime
from collections import Counter

# Import strict mode for fatal error handling
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import strict_mode

def generate_summary_report(classified_items: list[dict], storage_result: dict) -> dict:
    """Generate summary report with key metrics"""
    
    # Aggregate statistics
    categories = [item.get('category') for item in classified_items]
    priorities = [item.get('priority') for item in classified_items]
    statuses = [item.get('status') for item in classified_items]
    
    category_counts = dict(Counter(categories))
    priority_counts = dict(Counter(priorities))
    status_counts = dict(Counter(statuses))
    
    # Calculate total quantity
    total_quantity = sum(
        item.get('metadata', {}).get('quantity', 0) 
        for item in classified_items
    )
    
    summary = {
        'report_type': 'summary',
        'total_items': len(classified_items),
        'total_quantity': total_quantity,
        'categories': category_counts,
        'priorities': priority_counts,
        'statuses': status_counts,
        'storage': storage_result
    }
    
    return summary

def generate_detailed_report(classified_items: list[dict], storage_result: dict) -> dict:
    """Generate detailed report with all items"""
    
    summary = generate_summary_report(classified_items, storage_result)
    
    detailed = {
        **summary,
        'report_type': 'detailed',
        'items': classified_items
    }
    
    return detailed

def generate_alerts_report(classified_items: list[dict], storage_result: dict) -> dict:
    """Generate alerts report focusing on critical items"""
    
    # Filter critical and high priority items
    critical_items = [
        item for item in classified_items 
        if item.get('priority') in ['CRITICAL', 'HIGH']
    ]
    
    # Filter out of stock items
    out_of_stock = [
        item for item in classified_items
        if item.get('status') == 'OUT_OF_STOCK'
    ]
    
    # Filter low stock items
    low_stock = [
        item for item in classified_items
        if item.get('status') == 'LOW_STOCK'
    ]
    
    # Generate recommendations
    recommendations = []
    
    if out_of_stock:
        recommendations.append({
            'severity': 'CRITICAL',
            'message': f"{len(out_of_stock)} items are out of stock",
            'action': 'Reorder immediately',
            'items': [item.get('metadata', {}).get('name') for item in out_of_stock]
        })
    
    if low_stock:
        recommendations.append({
            'severity': 'HIGH',
            'message': f"{len(low_stock)} items are low in stock",
            'action': 'Plan reorder soon',
            'items': [item.get('metadata', {}).get('name') for item in low_stock]
        })
    
    alerts = {
        'report_type': 'alerts',
        'total_items': len(classified_items),
        'critical_count': len(critical_items),
        'out_of_stock_count': len(out_of_stock),
        'low_stock_count': len(low_stock),
        'critical_items': critical_items,
        'recommendations': recommendations,
        'storage': storage_result
    }
    
    return alerts

def run(**kwargs) -> dict:
    """
    Main entry point for m4_inventory_reporter module
    
    Args:
        storage_result: Storage metadata from m3
        classified_items: Classified items from m2
        report_format: Type of report ('summary', 'detailed', 'alerts')
    
    Returns:
        Final inventory report
    """
    storage_result = kwargs.get('storage_result')
    classified_items = kwargs.get('classified_items')
    report_format = kwargs.get('report_format', 'summary')
    
    if not storage_result:
        raise ValueError("⊥ storage_result is required")
    
    if not classified_items:
        raise ValueError("⊥ classified_items is required")
    
    print(f"📊 APT m4_inventory_reporter")
    print(f"   Input: storage_result = {storage_result.get('path')}")
    print(f"   Input: classified_items count = {len(classified_items)}")
    print(f"   Input: report_format = {report_format}")
    
    # Generate report based on format
    if report_format == 'summary':
        report = generate_summary_report(classified_items, storage_result)
    elif report_format == 'detailed':
        report = generate_detailed_report(classified_items, storage_result)
    elif report_format == 'alerts':
        report = generate_alerts_report(classified_items, storage_result)
    else:
        raise ValueError(f"⊥ Invalid report_format: {report_format}. Must be 'summary', 'detailed', or 'alerts'")
    
    # Add report metadata
    report['report_timestamp'] = datetime.now().isoformat()
    report['report_generated_by'] = 'APT_InventoryAI_m4_reporter'
    
    print(f"   Output: report type = {report.get('report_type')}")
    print(f"   Total items: {report.get('total_items')}")
    if 'recommendations' in report:
        print(f"   Recommendations: {len(report.get('recommendations'))}")
    print(f"✅ m4_inventory_reporter complete: Y = m4(y3, y2, format={report_format})")
    
    return report

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
        },
        {
            'item_id': 'SCAN_003',
            'classification_timestamp': datetime.now().isoformat(),
            'category': 'Components',
            'priority': 'CRITICAL',
            'status': 'OUT_OF_STOCK',
            'metadata': {'name': 'Part C', 'quantity': 0, 'location': 'Warehouse A'}
        }
    ]
    
    test_storage_result = {
        'path': '/tmp/test_inventory.json',
        'format': 'json',
        'size_bytes': 1024,
        'checksum': 'abc123',
        'storage_timestamp': datetime.now().isoformat()
    }
    
    # Test different report formats
    for fmt in ['summary', 'detailed', 'alerts']:
        print(f"\n{'='*60}")
        print(f"Testing {fmt} report:")
        print(f"{'='*60}")
        result = run(
            storage_result=test_storage_result,
            classified_items=test_classified_items,
            report_format=fmt
        )
        print(f"\nReport keys: {list(result.keys())}")
        if 'recommendations' in result:
            print(f"Recommendations: {result['recommendations']}")
