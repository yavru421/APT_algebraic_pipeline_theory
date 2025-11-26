#!/usr/bin/env python3
"""
Mock Vulnerable Server for APT Pipeline Testing
Simulates vulnerabilities without running a real server
"""

import json
import re
from urllib.parse import urlparse, parse_qs

class MockVulnerableServer:
    """Mock server that simulates vulnerable responses"""

    def __init__(self):
        self.routes = {
            '/': self.home,
            '/login': self.login,
            '/search': self.search,
            '/user/1': self.user_profile_1,
            '/user/2': self.user_profile_2,
            '/redirect': self.redirect,
            '/file': self.file_access
        }

    def get_response(self, url: str, method: str = 'GET', params: dict = None, data: dict = None) -> dict:
        """Get mock response for a request"""
        parsed = urlparse(url)
        path = parsed.path or '/'

        # Add query params to params dict
        if parsed.query:
            query_params = parse_qs(parsed.query)
            if params:
                params.update({k: v[0] if v else '' for k, v in query_params.items()})
            else:
                params = {k: v[0] if v else '' for k, v in query_params.items()}

        # Route to appropriate handler
        for route, handler in self.routes.items():
            if path == route or (route.endswith('*') and path.startswith(route[:-1])):
                return handler(method, params or {}, data or {})

        # Default 404
        return {
            'status_code': 404,
            'text': 'Not Found',
            'headers': {}
        }

    def home(self, method, params, data):
        return {
            'status_code': 200,
            'text': '<html><body><h1>Welcome</h1><a href="/login">Login</a></body></html>',
            'headers': {'Content-Type': 'text/html'}
        }

    def login(self, method, params, data):
        if method == 'POST':
            username = data.get('username', '')
            password = data.get('password', '')

            # VULNERABLE: SQL Injection simulation
            if "' OR '1'='1" in username or "' OR '1'='1" in password:
                return {
                    'status_code': 200,
                    'text': 'Welcome admin!',
                    'headers': {}
                }
            elif username == 'admin' and password == 'password123':
                return {
                    'status_code': 200,
                    'text': 'Welcome admin!',
                    'headers': {}
                }
            else:
                return {
                    'status_code': 200,
                    'text': 'Login failed',
                    'headers': {}
                }

        return {
            'status_code': 200,
            'text': '<html><body><form method="POST"><input name="username"><input name="password"><input type="submit"></form></body></html>',
            'headers': {'Content-Type': 'text/html'}
        }

    def search(self, method, params, data):
        query = params.get('q', '')

        # VULNERABLE: XSS simulation
        if '<script>' in query:
            return {
                'status_code': 200,
                'text': f'<html><body>Results for: {query}</body></html>',
                'headers': {'Content-Type': 'text/html'}
            }

        return {
            'status_code': 200,
            'text': f'<html><body>Results for: {query}</body></html>',
            'headers': {'Content-Type': 'text/html'}
        }

    def user_profile_1(self, method, params, data):
        # VULNERABLE: IDOR - shows user 1's data
        return {
            'status_code': 200,
            'text': '<html><body><h2>User Profile</h2><p>ID: 1</p><p>Username: admin</p><p>Email: admin@test.com</p></body></html>',
            'headers': {'Content-Type': 'text/html'}
        }

    def user_profile_2(self, method, params, data):
        # VULNERABLE: IDOR - shows user 2's data (should be protected)
        return {
            'status_code': 200,
            'text': '<html><body><h2>User Profile</h2><p>ID: 2</p><p>Username: user</p><p>Email: user@test.com</p></body></html>',
            'headers': {'Content-Type': 'text/html'}
        }

    def redirect(self, method, params, data):
        url = params.get('url', '/')

        # VULNERABLE: Open Redirect
        return {
            'status_code': 302,
            'text': '',
            'headers': {'Location': url}
        }

    def file_access(self, method, params, data):
        filename = params.get('file', '')

        # VULNERABLE: Directory Traversal simulation
        if '../' in filename or '..\\' in filename:
            return {
                'status_code': 200,
                'text': 'Mock file content: root:x:0:0:root:/root:/bin/bash',
                'headers': {'Content-Type': 'text/plain'}
            }

        return {
            'status_code': 200,
            'text': 'File content',
            'headers': {'Content-Type': 'text/plain'}
        }

# Test the mock server
if __name__ == '__main__':
    server = MockVulnerableServer()

    # Test cases
    tests = [
        ('http://localhost:5000/', 'GET'),
        ('http://localhost:5000/login', 'GET'),
        ('http://localhost:5000/login', 'POST', {}, {'username': "' OR '1'='1 --", 'password': 'test'}),
        ('http://localhost:5000/search?q=<script>alert(1)</script>', 'GET'),
        ('http://localhost:5000/user/1', 'GET'),
        ('http://localhost:5000/user/2', 'GET'),
        ('http://localhost:5000/redirect?url=http://evil.com', 'GET'),
        ('http://localhost:5000/file?file=../../../etc/passwd', 'GET'),
    ]

    print("🧪 Testing Mock Vulnerable Server")
    for url, method, *args in tests:
        params = args[0] if len(args) > 0 else {}
        data = args[1] if len(args) > 1 else {}
        response = server.get_response(url, method, params, data)
        print(f"{method} {url} -> {response['status_code']}: {response['text'][:50]}...")