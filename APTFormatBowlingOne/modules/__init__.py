# APT Bowling Scheduler Modules
# Algebraic Pipeline Theory - Modular Implementation
# Version: 1.0.0

"""
APT Bowling Scheduler Modules Package

This package contains all 16 modules (m0-m15) that implement the
Algebraic Pipeline Theory for bowling score analysis and management.

Each module follows the APT specification defined in:
../bowling_scheduler_system.rapt

Module Structure:
- m0-m1: File operations (DNG conversion, UI)
- m2-m6: Core processing (upload, API, parse, display, EXIF)  
- m7-m9: Data presentation (metadata, batch, calendar)
- m10-m11: Analytics (leaderboard, table)
- m12-m15: Persistence (save, load, smart, cleanup)

All modules are designed to be:
- Transparent: Clear algebraic relationships
- Reproducible: Same inputs produce same outputs
- Modular: Can be tested and used independently
- Traceable: All operations are logged
"""

__version__ = "1.0.0"
__author__ = "APT System"
__description__ = "Algebraic Pipeline Theory Bowling Scheduler Modules"