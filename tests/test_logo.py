#!/usr/bin/env python3
"""
Test script to verify logo handling in Borel.
"""

import base64
from pathlib import Path

def test_logo_conversion():
    """Test logo file to base64 conversion."""
    print("Testing logo conversion...")
    
    # Test with the SVG logo we created
    logo_path = "examples/test-logo.svg"
    
    if not Path(logo_path).exists():
        print(f"❌ Logo file not found: {logo_path}")
        return False
    
    try:
        with open(logo_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            # Determine MIME type
            ext = Path(logo_path).suffix.lower()
            if ext == '.svg':
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'image/png'
            
            data_url = f"data:{mime_type};base64,{base64_data}"
            
            print(f"✅ Logo converted successfully")
            print(f"   File: {logo_path}")
            print(f"   Size: {len(image_data)} bytes")
            print(f"   MIME: {mime_type}")
            print(f"   Data URL length: {len(data_url)} characters")
            
            return True
            
    except Exception as e:
        print(f"❌ Logo conversion failed: {e}")
        return False

def test_css_generation():
    """Test CSS generation with logo."""
    print("\nTesting CSS generation...")
    
    # Simulate the CSS generation from PDF generator
    logo_path = "examples/test-logo.svg"
    
    if not Path(logo_path).exists():
        print(f"❌ Logo file not found: {logo_path}")
        return False
    
    try:
        with open(logo_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            
            ext = Path(logo_path).suffix.lower()
            if ext == '.svg':
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'image/png'
            
            data_url = f"data:{mime_type};base64,{base64_data}"
            
            # Generate CSS like the PDF generator does
            logo_css = f"""
            .letterhead {{
                content: url({data_url});
                position: fixed;
                top: 1cm;
                right: 1cm;
                width: 3cm;
                height: auto;
                z-index: 1000;
            }}
            """
            
            print(f"✅ CSS generated successfully")
            print(f"   CSS length: {len(logo_css)} characters")
            print(f"   Contains data URL: {'data:' in logo_css}")
            
            return True
            
    except Exception as e:
        print(f"❌ CSS generation failed: {e}")
        return False

def main():
    """Run all logo tests."""
    print("Borel Logo Test")
    print("=" * 50)
    
    tests = [
        test_logo_conversion,
        test_css_generation
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
        print("✅ All logo tests passed!")
        print("\nTo test with Docker:")
        print("./scripts/borel-docker.sh --verbose examples/sample.md")
        return 0
    else:
        print("❌ Some logo tests failed.")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main()) 