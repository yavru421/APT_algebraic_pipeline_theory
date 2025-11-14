#!/usr/bin/env python3
"""
APT Strict Mode - Fatal Enforcement Module
Algebraic Pipeline Theory - Exceptions are ⊥

This module enforces fatal error propagation. Any unhandled exception halts execution immediately.
"""

import sys
import traceback

def strict_excepthook(exc_type, exc_value, exc_tb):
    print(f"\n❌ APT FATAL ERROR: {exc_type.__name__} – {exc_value}")
    traceback.print_tb(exc_tb)
    sys.exit(1)

# Override default exception handler
sys.excepthook = strict_excepthook

print("⚙️ APT Fatal Mode Active: All exceptions are terminal.")