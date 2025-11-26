#!/usr/bin/env python3
"""
Test the Advanced APT Bug Hunting Pipeline against vulnerable test app
"""

import sys
import os
from urllib.parse import urlparse
sys.path.append(os.path.dirname(__file__))

from APT_MODULES.m7_advanced_bug_hunter import execute_advanced_bug_hunting, AdvancedBurpScopeManager

if __name__ == "__main__":
    # Debug scope first
    print("🔍 Debugging scope configuration...")
    scope_manager = AdvancedBurpScopeManager('test_scope.json')

    test_urls = [
        'http://127.0.0.1:5000',
        'http://localhost:5000'
    ]

    for url in test_urls:
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or '/'
        port = str(parsed.port or (443 if parsed.scheme == 'https' else 80))
        protocol = parsed.scheme

        print(f"   URL: {url}")
        print(f"     Parsed - host: '{host}', path: '{path}', port: '{port}', protocol: '{protocol}'")

        in_scope = scope_manager.is_in_scope(url)
        print(f"     Result: in_scope = {in_scope}")
        print()

    print()

    # Test against our vulnerable local app
    burp_config_path = 'test_scope.json'
    targets = [
        'http://127.0.0.1:5000',
        'http://localhost:5000'
    ]

    print("🧪 Testing APT Advanced Bug Hunting Pipeline")
    print("   Against: Vulnerable Test Application")
    print("   Target: http://localhost:5000")
    print("   Known vulnerabilities: SQLi, XSS, IDOR, Open Redirect, Directory Traversal")
    print("=" * 80)

    report = execute_advanced_bug_hunting(burp_config_path, targets)