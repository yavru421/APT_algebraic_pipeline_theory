#!/usr/bin/env python3
"""
APT InventoryAI Pipeline Executor
Executes the algebraic pipeline: Y = m4(m3(m2(m1(X))))

This executor follows APT principles:
- Modular pipeline execution
- Explicit I/O tracking
- Fatal error handling
- Full traceability
"""

import sys
import os
import yaml
import json
import importlib
from datetime import datetime
from pathlib import Path

# Import strict mode for fatal error handling
import strict_mode

def load_pipeline_config(config_path: str) -> dict:
    """Load pipeline configuration from YAML"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"⊥ Pipeline config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'pipeline' not in config:
        raise ValueError("⊥ Invalid pipeline config: missing 'pipeline' key")
    
    return config

def resolve_arg(arg_value, pipeline_outputs: dict):
    """Resolve pipeline variable references like $m1_scanner"""
    if isinstance(arg_value, str) and arg_value.startswith('$'):
        var_name = arg_value[1:]  # Remove $
        if var_name not in pipeline_outputs:
            raise ValueError(f"⊥ Undefined pipeline variable: {arg_value}")
        return pipeline_outputs[var_name]
    elif isinstance(arg_value, dict):
        return {k: resolve_arg(v, pipeline_outputs) for k, v in arg_value.items()}
    elif isinstance(arg_value, list):
        return [resolve_arg(v, pipeline_outputs) for v in arg_value]
    else:
        return arg_value

def execute_module(module_spec: dict, pipeline_outputs: dict) -> any:
    """Execute a single pipeline module"""
    module_name = module_spec.get('module')
    fn_name = module_spec.get('fn', 'run')
    args = module_spec.get('args', {})
    name = module_spec.get('name')
    
    print(f"\n{'='*80}")
    print(f"Executing module: {name} ({module_name}.{fn_name})")
    print(f"{'='*80}")
    
    # Resolve arguments
    resolved_args = {}
    for key, value in args.items():
        resolved_args[key] = resolve_arg(value, pipeline_outputs)
    
    # Import and execute module
    try:
        module = importlib.import_module(module_name)
        fn = getattr(module, fn_name)
        result = fn(**resolved_args)
        return result
    except Exception as e:
        print(f"⊥ FATAL ERROR in module {name}: {e}")
        raise

def execute_pipeline(config_path: str) -> dict:
    """Execute the complete APT pipeline"""
    print(f"\n🚀 APT InventoryAI Pipeline Starting")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"📄 Config: {config_path}")
    print(f"{'='*80}\n")
    
    # Load configuration
    config = load_pipeline_config(config_path)
    pipeline = config['pipeline']
    
    # Execute pipeline modules in sequence
    pipeline_outputs = {}
    
    for module_spec in pipeline:
        name = module_spec.get('name')
        result = execute_module(module_spec, pipeline_outputs)
        pipeline_outputs[name] = result
    
    print(f"\n{'='*80}")
    print(f"✅ APT InventoryAI Pipeline Complete")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"{'='*80}\n")
    
    # Return final output
    final_module = pipeline[-1]['name']
    return pipeline_outputs[final_module]

def save_pipeline_trace(result: dict, trace_path: str):
    """Save pipeline execution trace"""
    trace_data = {
        'timestamp': datetime.now().isoformat(),
        'pipeline': 'InventoryAI',
        'equation': 'Y = m4(m3(m2(m1(X))))',
        'result': result
    }
    
    os.makedirs(os.path.dirname(trace_path), exist_ok=True)
    with open(trace_path, 'w') as f:
        json.dump(trace_data, f, indent=2)
    
    print(f"📝 Pipeline trace saved to: {trace_path}")

if __name__ == "__main__":
    # Default config path
    config_path = "APT_PIPELINE_INVENTORY.yaml"
    
    # Allow override from command line
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    try:
        # Execute pipeline
        result = execute_pipeline(config_path)
        
        # Save trace
        trace_path = f"APT_PIPELINE_RUNS/inventory_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_pipeline_trace(result, trace_path)
        
        # Print summary
        print(f"\n📊 Final Report Summary:")
        print(f"   Report Type: {result.get('report_type')}")
        print(f"   Total Items: {result.get('total_items')}")
        print(f"   Generated: {result.get('report_timestamp')}")
        
        if 'recommendations' in result and result['recommendations']:
            print(f"\n🚨 Recommendations:")
            for rec in result['recommendations']:
                print(f"   [{rec['severity']}] {rec['message']}")
                print(f"   Action: {rec['action']}")
        
        print(f"\n✅ InventoryAI pipeline execution successful")
        
    except Exception as e:
        print(f"\n❌ Pipeline execution failed")
        print(f"⊥ FATAL ERROR: {e}")
        sys.exit(1)
