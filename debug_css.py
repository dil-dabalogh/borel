#!/usr/bin/env python3
"""
Debug script to test CSS loading and logo handling.
"""

import os
import sys
from pathlib import Path

def test_css_loading():
    """Test CSS file loading."""
    print("Testing CSS loading...")
    
    css_path = "examples/diligent-branding.css"
    
    if not os.path.exists(css_path):
        print(f"❌ CSS file not found: {css_path}")
        return False
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        print(f"✅ CSS loaded successfully")
        print(f"   File: {css_path}")
        print(f"   Size: {len(css_content)} characters")
        print(f"   Contains Diligent colors: {'--diligent-red-primary' in css_content}")
        print(f"   Contains letterhead: {'.letterhead' in css_content}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSS loading failed: {e}")
        return False

def test_config_loading():
    """Test config file loading."""
    print("\nTesting config loading...")
    
    config_path = "examples/borel.config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Config loaded successfully")
        print(f"   CSS file: {config.get('css_file', 'N/A')}")
        print(f"   Logo file: {config.get('logo_file', 'N/A')}")
        print(f"   Company: {config.get('company_name', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_logo_file():
    """Test logo file existence."""
    print("\nTesting logo file...")
    
    logo_path = "examples/test-logo.svg"
    
    if not os.path.exists(logo_path):
        print(f"❌ Logo file not found: {logo_path}")
        return False
    
    try:
        with open(logo_path, 'r') as f:
            logo_content = f.read()
        
        print(f"✅ Logo file found")
        print(f"   File: {logo_path}")
        print(f"   Size: {len(logo_content)} characters")
        print(f"   Contains SVG: {'<svg' in logo_content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Logo file check failed: {e}")
        return False

def main():
    """Run all debug tests."""
    print("Borel CSS Debug Test")
    print("=" * 50)
    
    tests = [
        test_css_loading,
        test_config_loading,
        test_logo_file
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Debug Results Summary:")
    
    if all(results):
        print("✅ All debug tests passed!")
        print("\nThe issue might be in the Docker container path resolution.")
        return 0
    else:
        print("❌ Some debug tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 