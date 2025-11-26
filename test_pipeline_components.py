#!/usr/bin/env python3
"""
Test APT Advanced Bug Hunting Pipeline with Mock Responses
Tests vulnerability detection without needing a live server
"""

import sys
import os
import json
from unittest.mock import Mock, patch
sys.path.append(os.path.dirname(__file__))

from APT_MODULES.m7_advanced_bug_hunter import (
    AdvancedPayloadGenerator,
    AdvancedVulnerabilityDetector,
    AdvancedBurpScopeManager
)

def test_sql_injection_detection():
    """Test SQL injection detection with mock responses"""
    print("🧪 Testing SQL Injection Detection...")

    detector = AdvancedVulnerabilityDetector()
    payload_gen = AdvancedPayloadGenerator()

    # Mock SQL injection vulnerable response
    sql_error_response = Mock()
    sql_error_response.status_code = 200
    sql_error_response.text = "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' OR '1'='1' -- ' at line 1"
    sql_error_response.elapsed.total_seconds.return_value = 0.1

    # Mock normal response
    normal_response = Mock()
    normal_response.status_code = 200
    normal_response.text = "Login successful"
    normal_response.elapsed.total_seconds.return_value = 0.1

    with patch.object(detector.session, 'get', side_effect=[sql_error_response, normal_response]):
        # Test SQL injection detection
        vuln = detector.test_sql_injection("http://test.com/login", {"username": "admin", "password": "pass"}, "username", "' OR '1'='1' --")

        if vuln:
            print("✅ SQL Injection detected!")
            print(f"   Type: {vuln['type']}")
            print(f"   Confidence: {vuln['confidence']}")
            print(f"   Evidence: {vuln['evidence']}")
            return True
        else:
            print("❌ SQL Injection not detected")
            return False

def test_xss_detection():
    """Test XSS detection with mock responses"""
    print("\n🧪 Testing XSS Detection...")

    detector = AdvancedVulnerabilityDetector()

    # Mock XSS vulnerable response (payload reflected without encoding)
    xss_response = Mock()
    xss_response.status_code = 200
    xss_response.text = "<script>alert('XSS')</script>"  # Payload reflected
    xss_response.elapsed.total_seconds.return_value = 0.1

    # Mock safe response (payload encoded)
    safe_response = Mock()
    safe_response.status_code = 200
    safe_response.text = "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"  # Payload encoded
    safe_response.elapsed.total_seconds.return_value = 0.1

    with patch.object(detector.session, 'get', side_effect=[xss_response, safe_response]):
        # Test XSS detection
        vuln = detector.test_xss("http://test.com/search", {"q": "test"}, "q", "<script>alert('XSS')</script>")

        if vuln:
            print("✅ XSS detected!")
            print(f"   Type: {vuln['type']}")
            print(f"   Confidence: {vuln['confidence']}")
            print(f"   Evidence: {vuln['evidence']}")
            return True
        else:
            print("❌ XSS not detected")
            return False

def test_open_redirect_detection():
    """Test open redirect detection with mock responses"""
    print("\n🧪 Testing Open Redirect Detection...")

    detector = AdvancedVulnerabilityDetector()

    # Mock redirect response
    redirect_response = Mock()
    redirect_response.status_code = 302
    redirect_response.headers = {'Location': 'http://evil.com'}
    redirect_response.elapsed.total_seconds.return_value = 0.1

    with patch.object(detector.session, 'get', return_value=redirect_response):
        # Test open redirect detection
        vuln = detector.test_open_redirect("http://test.com/redirect", {"url": "http://test.com"}, "url")

        if vuln:
            print("✅ Open Redirect detected!")
            print(f"   Type: {vuln['type']}")
            print(f"   Confidence: {vuln['confidence']}")
            print(f"   Evidence: {vuln['evidence']}")
            return True
        else:
            print("❌ Open Redirect not detected")
            return False

def test_payload_generation():
    """Test payload generation"""
    print("\n🧪 Testing Payload Generation...")

    gen = AdvancedPayloadGenerator()

    sqli_payloads = gen.get_payloads_for_type('sqli')
    xss_payloads = gen.get_payloads_for_type('xss')
    cmdi_payloads = gen.get_payloads_for_type('cmdi')

    print(f"   SQLi payloads: {len(sqli_payloads)}")
    print(f"   XSS payloads: {len(xss_payloads)}")
    print(f"   CMDi payloads: {len(cmdi_payloads)}")

    # Check that we have actual payloads
    if len(sqli_payloads) > 0 and len(xss_payloads) > 0 and len(cmdi_payloads) > 0:
        print("✅ Payload generation working")
        return True
    else:
        print("❌ Payload generation failed")
        return False

def test_scope_manager():
    """Test scope manager functionality"""
    print("\n🧪 Testing Scope Manager...")

    # Create test scope config
    scope_config = {
        "target": {
            "scope": {
                "include": [
                    {
                        "enabled": True,
                        "host": "^test\\.com$",
                        "file": "^/.*",
                        "port": "^80$",
                        "protocol": "http"
                    }
                ],
                "exclude": []
            }
        }
    }

    # Mock file reading
    with patch('builtins.open', create=True) as mock_open:
        mock_file = Mock()
        mock_file.read.return_value = json.dumps(scope_config)
        mock_open.return_value.__enter__.return_value = mock_file

        scope_manager = AdvancedBurpScopeManager("dummy.json")

        # Test in-scope URL
        in_scope = scope_manager.is_in_scope("http://test.com/page")
        print(f"   http://test.com/page in scope: {in_scope}")

        # Test out-of-scope URL
        out_scope = scope_manager.is_in_scope("http://evil.com/page")
        print(f"   http://evil.com/page in scope: {out_scope}")

        if in_scope and not out_scope:
            print("✅ Scope manager working correctly")
            return True
        else:
            print("❌ Scope manager failed")
            return False

def main():
    """Run all tests"""
    print("🚀 Testing APT Advanced Bug Hunting Pipeline Components")
    print("=" * 60)

    results = []

    # Test individual components
    results.append(test_payload_generation())
    results.append(test_scope_manager())
    results.append(test_sql_injection_detection())
    results.append(test_xss_detection())
    results.append(test_open_redirect_detection())

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ APT Advanced Bug Hunting Pipeline is functional")
        print("✅ Vulnerability detection components working")
        print("✅ Scope management working")
        print("✅ Ready for real-world testing")
    else:
        print("❌ Some tests failed")
        print("🔧 Pipeline needs debugging")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)