#!/usr/bin/env python3
"""
Test Suite for InventoryAI APT Pipeline
Tests all modules and end-to-end pipeline execution

Following APT principles:
- Fatal error handling (no graceful failures)
- Explicit I/O validation
- Module contract testing
"""

import sys
import os
import json
import pytest
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import modules
from APT_MODULES import m1_inventory_scanner
from APT_MODULES import m2_inventory_classifier
from APT_MODULES import m3_inventory_storage
from APT_MODULES import m4_inventory_reporter

# Test data
TEST_INVENTORY_DATA = {
    "items": [
        {"id": 1, "name": "Widget A", "quantity": 100, "location": "Warehouse A"},
        {"id": 2, "name": "Tool B", "quantity": 5, "location": "Warehouse B"},
        {"id": 3, "name": "Part C", "quantity": 0, "location": "Warehouse A"}
    ]
}

class TestM1InventoryScanner:
    """Test m1_inventory_scanner module"""
    
    def setup_method(self):
        """Create test data file"""
        self.test_file = "/tmp/test_inventory_scanner.json"
        with open(self.test_file, 'w') as f:
            json.dump(TEST_INVENTORY_DATA, f)
    
    def teardown_method(self):
        """Clean up test files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_scan_file_success(self):
        """Test successful file scanning"""
        result = m1_inventory_scanner.run(
            inventory_path=self.test_file,
            scan_type='file'
        )
        
        assert isinstance(result, list)
        assert len(result) == 3
        assert all('scan_id' in item for item in result)
        assert all('scan_timestamp' in item for item in result)
        assert all('raw_data' in item for item in result)
    
    def test_scan_file_not_found(self):
        """Test fatal error on missing file"""
        with pytest.raises(FileNotFoundError):
            m1_inventory_scanner.run(
                inventory_path="/nonexistent/file.json",
                scan_type='file'
            )
    
    def test_scan_invalid_type(self):
        """Test fatal error on invalid scan type"""
        with pytest.raises(ValueError):
            m1_inventory_scanner.run(
                inventory_path=self.test_file,
                scan_type='invalid'
            )
    
    def test_scan_missing_path(self):
        """Test fatal error on missing path"""
        with pytest.raises(ValueError):
            m1_inventory_scanner.run(scan_type='file')

class TestM2InventoryClassifier:
    """Test m2_inventory_classifier module"""
    
    def setup_method(self):
        """Create test scanned items"""
        self.test_scanned_items = [
            {
                'scan_id': 'SCAN_001',
                'scan_timestamp': datetime.now().isoformat(),
                'raw_data': {'name': 'Widget A', 'quantity': 100, 'location': 'Warehouse A'}
            },
            {
                'scan_id': 'SCAN_002',
                'scan_timestamp': datetime.now().isoformat(),
                'raw_data': {'name': 'Tool B', 'quantity': 5, 'location': 'Warehouse B'}
            }
        ]
    
    def test_classify_success(self):
        """Test successful classification"""
        result = m2_inventory_classifier.run(
            scanned_items=self.test_scanned_items
        )
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert all('category' in item for item in result)
        assert all('priority' in item for item in result)
        assert all('status' in item for item in result)
    
    def test_classify_custom_rules(self):
        """Test classification with custom rules"""
        custom_rules = {
            'default_category': 'Custom',
            'low_stock_threshold': 10
        }
        
        result = m2_inventory_classifier.run(
            scanned_items=self.test_scanned_items,
            classification_rules=custom_rules
        )
        
        assert len(result) == 2
        # Tool B with quantity 5 should be HIGH priority with threshold 10
        tool_b = next(item for item in result if 'Tool' in item['metadata']['name'])
        assert tool_b['priority'] == 'HIGH'
    
    def test_classify_empty_items(self):
        """Test fatal error on empty items"""
        with pytest.raises(ValueError):
            m2_inventory_classifier.run(scanned_items=[])
    
    def test_classify_invalid_items(self):
        """Test fatal error on invalid items"""
        with pytest.raises(ValueError):
            m2_inventory_classifier.run(scanned_items="not a list")

class TestM3InventoryStorage:
    """Test m3_inventory_storage module"""
    
    def setup_method(self):
        """Create test classified items"""
        self.test_classified_items = [
            {
                'item_id': 'SCAN_001',
                'classification_timestamp': datetime.now().isoformat(),
                'category': 'Electronics',
                'priority': 'LOW',
                'status': 'IN_STOCK',
                'metadata': {'name': 'Widget A', 'quantity': 100, 'location': 'Warehouse A'}
            }
        ]
        self.test_output_json = "/tmp/test_storage_output.json"
        self.test_output_csv = "/tmp/test_storage_output.csv"
    
    def teardown_method(self):
        """Clean up test files"""
        for f in [self.test_output_json, self.test_output_csv]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_storage_json_success(self):
        """Test successful JSON storage"""
        result = m3_inventory_storage.run(
            classified_items=self.test_classified_items,
            storage_path=self.test_output_json,
            storage_format='json'
        )
        
        assert result['format'] == 'json'
        assert result['path'] == self.test_output_json
        assert os.path.exists(self.test_output_json)
        assert 'checksum' in result
        assert 'size_bytes' in result
        assert result['item_count'] == 1
    
    def test_storage_csv_success(self):
        """Test successful CSV storage"""
        result = m3_inventory_storage.run(
            classified_items=self.test_classified_items,
            storage_path=self.test_output_csv,
            storage_format='csv'
        )
        
        assert result['format'] == 'csv'
        assert result['path'] == self.test_output_csv
        assert os.path.exists(self.test_output_csv)
    
    def test_storage_empty_items(self):
        """Test fatal error on empty items"""
        with pytest.raises(ValueError):
            m3_inventory_storage.run(
                classified_items=[],
                storage_path=self.test_output_json
            )
    
    def test_storage_invalid_format(self):
        """Test fatal error on invalid format"""
        with pytest.raises(ValueError):
            m3_inventory_storage.run(
                classified_items=self.test_classified_items,
                storage_path=self.test_output_json,
                storage_format='xml'
            )

class TestM4InventoryReporter:
    """Test m4_inventory_reporter module"""
    
    def setup_method(self):
        """Create test data"""
        self.test_classified_items = [
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
                'priority': 'CRITICAL',
                'status': 'OUT_OF_STOCK',
                'metadata': {'name': 'Tool B', 'quantity': 0, 'location': 'Warehouse B'}
            }
        ]
        self.test_storage_result = {
            'path': '/tmp/test_inventory.json',
            'format': 'json',
            'size_bytes': 1024,
            'checksum': 'abc123',
            'storage_timestamp': datetime.now().isoformat()
        }
    
    def test_report_summary(self):
        """Test summary report generation"""
        result = m4_inventory_reporter.run(
            storage_result=self.test_storage_result,
            classified_items=self.test_classified_items,
            report_format='summary'
        )
        
        assert result['report_type'] == 'summary'
        assert result['total_items'] == 2
        assert 'categories' in result
        assert 'priorities' in result
        assert 'statuses' in result
    
    def test_report_detailed(self):
        """Test detailed report generation"""
        result = m4_inventory_reporter.run(
            storage_result=self.test_storage_result,
            classified_items=self.test_classified_items,
            report_format='detailed'
        )
        
        assert result['report_type'] == 'detailed'
        assert 'items' in result
        assert len(result['items']) == 2
    
    def test_report_alerts(self):
        """Test alerts report generation"""
        result = m4_inventory_reporter.run(
            storage_result=self.test_storage_result,
            classified_items=self.test_classified_items,
            report_format='alerts'
        )
        
        assert result['report_type'] == 'alerts'
        assert result['out_of_stock_count'] == 1
        assert len(result['recommendations']) > 0
        assert any(rec['severity'] == 'CRITICAL' for rec in result['recommendations'])
    
    def test_report_invalid_format(self):
        """Test fatal error on invalid format"""
        with pytest.raises(ValueError):
            m4_inventory_reporter.run(
                storage_result=self.test_storage_result,
                classified_items=self.test_classified_items,
                report_format='invalid'
            )

class TestEndToEndPipeline:
    """Test complete pipeline execution"""
    
    def setup_method(self):
        """Create test environment"""
        self.test_input_file = "/tmp/test_e2e_inventory.json"
        self.test_output_file = "/tmp/test_e2e_output.json"
        
        test_data = {
            "items": [
                {"id": 1, "name": "Widget A", "quantity": 100, "location": "Warehouse A"},
                {"id": 2, "name": "Tool B", "quantity": 5, "location": "Warehouse B"},
                {"id": 3, "name": "Part C", "quantity": 0, "location": "Warehouse A"}
            ]
        }
        
        with open(self.test_input_file, 'w') as f:
            json.dump(test_data, f)
    
    def teardown_method(self):
        """Clean up test files"""
        for f in [self.test_input_file, self.test_output_file]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_full_pipeline(self):
        """Test complete pipeline: Y = m4(m3(m2(m1(X))))"""
        # m1: Scan
        y1 = m1_inventory_scanner.run(
            inventory_path=self.test_input_file,
            scan_type='file'
        )
        assert len(y1) == 3
        
        # m2: Classify
        y2 = m2_inventory_classifier.run(scanned_items=y1)
        assert len(y2) == 3
        assert all('category' in item for item in y2)
        
        # m3: Store
        y3 = m3_inventory_storage.run(
            classified_items=y2,
            storage_path=self.test_output_file,
            storage_format='json'
        )
        assert os.path.exists(self.test_output_file)
        
        # m4: Report
        Y = m4_inventory_reporter.run(
            storage_result=y3,
            classified_items=y2,
            report_format='alerts'
        )
        assert Y['total_items'] == 3
        assert Y['out_of_stock_count'] == 1
        
        # Verify algebraic composition
        assert Y['report_type'] == 'alerts'
        print(f"✅ Pipeline Y = m4(m3(m2(m1(X)))) executed successfully")

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
