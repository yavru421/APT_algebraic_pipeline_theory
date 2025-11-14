#!/usr/bin/env python3
"""
Debug Burp Scope Rules
"""

import json
import re
from urllib.parse import urlparse

def debug_scope_rules(config_path: str):
    """Debug Burp scope rules to understand why URLs are rejected"""
    with open(config_path, 'r') as f:
        config = json.load(f)

    scope = config['target']['scope']
    include_rules = [rule for rule in scope['include'] if rule['enabled']]
    exclude_rules = [rule for rule in scope['exclude'] if rule['enabled']]

    print(f"Include rules: {len(include_rules)}")
    print(f"Exclude rules: {len(exclude_rules)}")
    print()

    # Show first few include rules
    print("First 5 include rules:")
    for i, rule in enumerate(include_rules[:5]):
        print(f"{i+1}. Host: {rule['host']}, File: {rule['file']}, Port: {rule['port']}, Protocol: {rule['protocol']}")
    print()

    # Test URLs
    test_urls = [
        'https://www.booking.com',
        'https://account.booking.com',
        'https://secure.booking.com',
        'https://www.fareharbor.com'
    ]

    for url in test_urls:
        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or '/'
        port = str(parsed.port or (443 if parsed.scheme == 'https' else 80))
        protocol = parsed.scheme

        print(f"Testing URL: {url}")
        print(f"  Host: {host}, Path: {path}, Port: {port}, Protocol: {protocol}")

        # Check excludes first
        excluded = False
        for rule in exclude_rules:
            try:
                host_pattern = re.compile(rule['host'], re.IGNORECASE)
                file_pattern = re.compile(rule['file'], re.IGNORECASE)
                port_pattern = re.compile(rule['port'])
                protocol_pattern = re.compile(rule['protocol'])

                if (host_pattern.match(host) and
                    file_pattern.match(path) and
                    port_pattern.match(port) and
                    protocol_pattern.match(protocol)):
                    print(f"  ❌ EXCLUDED by rule: {rule['host']}")
                    excluded = True
                    break
            except re.error as e:
                print(f"  Regex error in exclude rule: {e}")
                continue

        if excluded:
            print("  Result: OUT OF SCOPE (excluded)")
            continue

        # Check includes
        included = False
        for rule in include_rules:
            try:
                host_pattern = re.compile(rule['host'], re.IGNORECASE)
                file_pattern = re.compile(rule['file'], re.IGNORECASE)
                port_pattern = re.compile(rule['port'])
                protocol_pattern = re.compile(rule['protocol'])

                if (host_pattern.match(host) and
                    file_pattern.match(path) and
                    port_pattern.match(port) and
                    protocol_pattern.match(protocol)):
                    print(f"  ✅ INCLUDED by rule: {rule['host']}")
                    included = True
                    break
            except re.error as e:
                print(f"  Regex error in include rule: {e}")
                continue

        if included:
            print("  Result: IN SCOPE")
        else:
            print("  Result: OUT OF SCOPE (no matching include rule)")
        print()

if __name__ == "__main__":
    debug_scope_rules('c:/Users/John/Downloads/bookingcom-2025-11-12T18_34_02Z.json')