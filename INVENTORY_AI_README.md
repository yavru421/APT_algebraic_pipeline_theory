# InventoryAI - APT Algebraic Pipeline System

## Overview

InventoryAI is a complete inventory management system built using Algebraic Pipeline Theory (APT) principles. It demonstrates modular pipeline construction, explicit I/O contracts, fatal error handling, and full traceability.

## Algebraic Pipeline Equation

```
Y = m4(m3(m2(m1(X))))
```

Where:
- **X** = Raw inventory data (JSON file or directory)
- **y1 = m1(X)** = Scanned inventory items with metadata
- **y2 = m2(y1)** = Classified items (category, priority, status)
- **y3 = m3(y2)** = Storage result with checksum
- **Y = m4(y3, y2)** = Final inventory report with recommendations

## Module Contracts

### m1_inventory_scanner

**Inputs:**
- `inventory_path`: str - Path to inventory data source
- `scan_type`: str - Type of scan ('file' or 'directory')

**Outputs:**
- `scanned_items`: list[dict] - Raw inventory items with scan metadata

**Errors:**
- `FileNotFoundError` - If path doesn't exist (⊥)
- `ValueError` - If scan_type is invalid (⊥)

**Success Criteria:**
Returns list of items with scan_id, scan_timestamp, and raw_data

**Algebraic:** `y1 = m1(x_path, x_scan_type)`

---

### m2_inventory_classifier

**Inputs:**
- `scanned_items`: list[dict] - Output from m1_inventory_scanner
- `classification_rules`: dict (optional) - Custom classification rules

**Outputs:**
- `classified_items`: list[dict] - Items with category, priority, and status

**Errors:**
- `ValueError` - If scanned_items is empty or invalid (⊥)

**Success Criteria:**
Returns items with classification metadata:
- **Category**: Electronics, Hardware, Components, RawMaterials, General
- **Priority**: CRITICAL (qty=0), HIGH (qty<20), MEDIUM (qty<50), LOW (qty>=50)
- **Status**: OUT_OF_STOCK, LOW_STOCK, NORMAL, IN_STOCK

**Algebraic:** `y2 = m2(y1, x_rules)`

---

### m3_inventory_storage

**Inputs:**
- `classified_items`: list[dict] - Output from m2_inventory_classifier
- `storage_path`: str - Path for storage
- `storage_format`: str - Format ('json' or 'csv')

**Outputs:**
- `storage_result`: dict - Storage metadata with checksum

**Errors:**
- `ValueError` - If classified_items is empty (⊥)
- `IOError` - If storage operation fails (⊥)

**Success Criteria:**
Data stored successfully with:
- SHA256 checksum
- File size
- Timestamp
- Item count

**Algebraic:** `y3 = m3(y2, x_path, x_format)`

---

### m4_inventory_reporter

**Inputs:**
- `storage_result`: dict - Output from m3_inventory_storage
- `classified_items`: list[dict] - For generating summary
- `report_format`: str - Report type ('summary', 'detailed', 'alerts')

**Outputs:**
- `report`: dict - Final inventory report with insights

**Errors:**
- `ValueError` - If inputs are invalid (⊥)

**Success Criteria:**
Returns comprehensive report with:
- **Summary**: Aggregate statistics by category, priority, status
- **Detailed**: Full item listing with all metadata
- **Alerts**: Critical items and actionable recommendations

**Algebraic:** `Y = m4(y3, y2, x_report_format)`

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Required packages: pyyaml, pandas, scikit-learn, xgboost

### Install Dependencies

```bash
cd /home/runner/work/APT_algebraic_pipeline_theory/APT_algebraic_pipeline_theory
pip install -r requirements.txt
```

### Directory Structure

```
APT_algebraic_pipeline_theory/
├── APT_MODULES/
│   ├── m1_inventory_scanner.py
│   ├── m2_inventory_classifier.py
│   ├── m3_inventory_storage.py
│   └── m4_inventory_reporter.py
├── APT_INPUTS/
│   └── inventory_data.json
├── APT_PIPELINE_RUNS/
│   ├── inventory_output.json
│   └── inventory_trace_*.json
├── APT_PIPELINE_INVENTORY.yaml
├── inventory_ai_pipeline.py
├── test_inventory_ai.py
└── strict_mode.py
```

## Usage

### Quick Start

Run the complete pipeline:

```bash
python3 inventory_ai_pipeline.py
```

### Custom Configuration

Modify `APT_PIPELINE_INVENTORY.yaml` to customize:
- Input data source
- Classification rules
- Storage format (JSON/CSV)
- Report type

Example:

```yaml
pipeline:
  - name: m1_scanner
    module: APT_MODULES.m1_inventory_scanner
    fn: run
    args:
      inventory_path: APT_INPUTS/my_inventory.json
      scan_type: file

  - name: m2_classifier
    module: APT_MODULES.m2_inventory_classifier
    fn: run
    args:
      scanned_items: $m1_scanner
      classification_rules:
        low_stock_threshold: 15
        medium_stock_threshold: 40

  - name: m3_storage
    module: APT_MODULES.m3_inventory_storage
    fn: run
    args:
      classified_items: $m2_classifier
      storage_path: APT_PIPELINE_RUNS/output.csv
      storage_format: csv

  - name: m4_reporter
    module: APT_MODULES.m4_inventory_reporter
    fn: run
    args:
      storage_result: $m3_storage
      classified_items: $m2_classifier
      report_format: alerts
```

### Running Individual Modules

Each module can be tested independently:

```bash
# Test scanner
python3 APT_MODULES/m1_inventory_scanner.py

# Test classifier
python3 APT_MODULES/m2_inventory_classifier.py

# Test storage
python3 APT_MODULES/m3_inventory_storage.py

# Test reporter
python3 APT_MODULES/m4_inventory_reporter.py
```

## Testing

Run the comprehensive test suite:

```bash
python3 -m pytest test_inventory_ai.py -v
```

Test coverage:
- ✅ 17 tests covering all modules
- ✅ Happy path scenarios
- ✅ Fatal error conditions (⊥)
- ✅ End-to-end pipeline validation
- ✅ Custom configuration testing

## APT Principles Applied

### 1. Modularity
Each module (m1-m4) is a discrete, testable unit with explicit contracts.

### 2. Explicitness
All variables, dependencies, and transformations are declared algebraically.

### 3. Traceability
Every execution produces:
- Timestamped outputs in `APT_PIPELINE_RUNS/`
- Full execution trace with algebraic equation
- Checksums for data integrity

### 4. Reproducibility
Same inputs + environment = same outputs
- Deterministic classification rules
- Version-locked dependencies
- Complete audit trail

### 5. Fatal Error Handling
No graceful failures. All errors halt execution immediately (⊥):
- Missing files → FileNotFoundError
- Invalid inputs → ValueError
- Storage failures → IOError

### 6. Composability
Modules chain algebraically using `$variable` notation in YAML.

## Sample Input Data

```json
{
  "items": [
    {
      "id": 1,
      "name": "Widget Pro X1",
      "quantity": 150,
      "location": "Warehouse A",
      "sku": "WDG-PRO-X1",
      "unit_cost": 25.99
    },
    {
      "id": 2,
      "name": "Tool Basic Hammer",
      "quantity": 5,
      "location": "Warehouse C",
      "sku": "TL-HAM-BAS",
      "unit_cost": 12.99
    }
  ]
}
```

## Sample Output Report

```json
{
  "report_type": "alerts",
  "total_items": 10,
  "critical_count": 6,
  "out_of_stock_count": 2,
  "low_stock_count": 4,
  "recommendations": [
    {
      "severity": "CRITICAL",
      "message": "2 items are out of stock",
      "action": "Reorder immediately",
      "items": ["Part Assembly A1", "Widget Deluxe D3"]
    },
    {
      "severity": "HIGH",
      "message": "4 items are low in stock",
      "action": "Plan reorder soon",
      "items": ["Tool Basic Hammer", "Part Component B2"]
    }
  ],
  "report_timestamp": "2025-11-14T16:03:41.716169",
  "storage": {
    "path": "APT_PIPELINE_RUNS/inventory_output.json",
    "checksum": "2eb9d96ad4a7cf67...",
    "size_bytes": 6932
  }
}
```

## Execution Trace

Every pipeline run generates a trace file:

```json
{
  "timestamp": "2025-11-14T16:03:41.716259",
  "pipeline": "InventoryAI",
  "equation": "Y = m4(m3(m2(m1(X))))",
  "result": { ... }
}
```

## Performance

- **Scan**: O(n) where n = number of items
- **Classify**: O(n) with constant-time rule matching
- **Store**: O(n) with SHA256 checksum computation
- **Report**: O(n) with aggregation

Typical execution: < 100ms for 1000 items

## Extending the System

### Add Custom Classification Rules

```python
custom_rules = {
    'category_patterns': {
        'premium': 'PremiumGoods',
        'bulk': 'BulkItems'
    },
    'low_stock_threshold': 10,
    'medium_stock_threshold': 30
}
```

### Add New Report Format

Edit `m4_inventory_reporter.py`:

```python
def generate_custom_report(classified_items, storage_result):
    # Your custom logic
    return custom_report
```

### Add Database Storage

Create `m5_database_sync.py`:

```python
def run(**kwargs):
    """Y' = m5(Y) - Sync to database"""
    # Database integration
```

## Troubleshooting

### Fatal Error: FileNotFoundError
- Verify `inventory_path` in YAML config
- Ensure input file exists in `APT_INPUTS/`

### Fatal Error: ValueError (empty items)
- Check input JSON structure
- Validate `items` array is not empty

### Module Import Errors
- Ensure Python path includes repository root
- Verify all dependencies installed

## Contributing

Follow APT principles:
1. Define module algebraically: inputs, outputs, equation
2. Document contract: inputs, outputs, errors, success criteria
3. Add tests: happy path + error conditions
4. Archive results with traceability

## License

MIT License - See repository LICENSE file

## Contact

For issues or questions, open a GitHub issue in the repository.

---

**InventoryAI - Inventory Management Through Algebraic Pipeline Theory**

*Y = m4(m3(m2(m1(X)))) - Reproducible, Traceable, Modular*
