#!/usr/bin/env python3
"""
Test script to verify Borel installation and dependencies.
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import click
        print("✅ Click imported successfully")
    except ImportError as e:
        print(f"❌ Click import failed: {e}")
        return False
    
    try:
        import pypandoc
        print("✅ PyPandoc imported successfully")
    except ImportError as e:
        print(f"❌ PyPandoc import failed: {e}")
        return False
    
    try:
        import weasyprint
        print("✅ WeasyPrint imported successfully")
    except ImportError as e:
        print(f"❌ WeasyPrint import failed: {e}")
        return False
    
    try:
        import jinja2
        print("✅ Jinja2 imported successfully")
    except ImportError as e:
        print(f"❌ Jinja2 import failed: {e}")
        return False
    
    try:
        import yaml
        print("✅ PyYAML imported successfully")
    except ImportError as e:
        print(f"❌ PyYAML import failed: {e}")
        return False
    
    return True

def test_pandoc():
    """Test if pandoc is available in the system."""
    print("\nTesting pandoc availability...")
    
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, check=True)
        print("✅ Pandoc is available")
        print(f"   Version: {result.stdout.split()[1]}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Pandoc not found: {e}")
        print("   Install pandoc with: brew install pandoc (macOS) or apt-get install pandoc (Ubuntu)")
        return False

def test_borel_module():
    """Test if the borel module can be imported."""
    print("\nTesting Borel module...")
    
    try:
        from borel import cli, processor, html_generator, pdf_generator, config
        print("✅ Borel modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Borel module import failed: {e}")
        return False

def test_sample_file():
    """Test if sample files exist."""
    print("\nTesting sample files...")
    
    sample_md = Path("examples/sample.md")
    sample_css = Path("examples/company-branding.css")
    sample_config = Path("examples/borel.config.json")
    
    if sample_md.exists():
        print("✅ Sample markdown file exists")
    else:
        print("❌ Sample markdown file not found")
        return False
    
    if sample_css.exists():
        print("✅ Sample CSS file exists")
    else:
        print("❌ Sample CSS file not found")
        return False
    
    if sample_config.exists():
        print("✅ Sample config file exists")
    else:
        print("❌ Sample config file not found")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Borel Installation Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_pandoc,
        test_borel_module,
        test_sample_file
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
    print("Test Results Summary:")
    
    if all(results):
        print("✅ All tests passed! Borel is ready to use.")
        print("\nTo get started:")
        print("1. Add to your .zshrc: source /path/to/borel/scripts/borel.zsh")
        print("2. Try: borel examples/sample.md")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nInstallation instructions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install pandoc: brew install pandoc (macOS) or apt-get install pandoc (Ubuntu)")
        print("3. Install borel: pip install -e .")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 