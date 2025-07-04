#!/usr/bin/env python3
"""
Test script to demonstrate the fixed logo and metadata functionality.
"""

import os
import tempfile
from pathlib import Path

# Add the borel package to the path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from borel.processor import MarkdownProcessor
from borel.html_generator import HTMLGenerator
from borel.config import BorelConfig

def create_test_files():
    """Create test files for demonstration."""
    
    # Create test markdown content
    markdown_content = """---
title: Test Document with Logo and Metadata
subtitle: Demonstrating the fixes
date: 2025-01-15
company_name: Diligent Corporation
author: David Balogh
---

# Introduction

This is a test document to demonstrate that the logo and metadata are now working correctly.

## Features Tested

- **Logo display** in the upper right corner
- **Title page** with proper metadata
- **Company branding** in footer
- **Page breaks** using [CRLF] tokens

[CRLF]

# Second Page

This content should appear on the second page with the logo visible.

## Metadata Verification

The following metadata should be displayed on the title page:
- Title: Test Document with Logo and Metadata
- Subtitle: Demonstrating the fixes  
- Date: 2025-01-15
- Company: Diligent Corporation
- Author: David Balogh

The logo should appear in the upper right corner of all pages except the title page.
"""

    # Create test CSS
    css_content = """/* Test CSS for logo and metadata */
@page {
    size: A4;
    margin: 2.5cm 2cm 2.5cm 2cm;
    
    @bottom-center {
        content: attr(data-company) " @ " attr(data-year);
        font-family: Arial, sans-serif;
        font-size: 9pt;
        color: #666;
        border-top: 1pt solid #ccc;
        padding-top: 0.2cm;
    }
    
    @bottom-right {
        content: counter(page);
        font-family: Arial, sans-serif;
        font-size: 9pt;
        color: #666;
        border-top: 1pt solid #ccc;
        padding-top: 0.2cm;
    }
}

body {
    font-family: Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #000;
}

h1 {
    font-size: 24pt;
    font-weight: bold;
    color: #EE312E;
    margin-top: 2em;
    margin-bottom: 1em;
    page-break-after: avoid;
    border-bottom: 2pt solid #EE312E;
    padding-bottom: 0.3em;
}

h2 {
    font-size: 18pt;
    font-weight: normal;
    color: #D3222A;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
    page-break-after: avoid;
}

.title-page {
    text-align: center;
    page-break-after: always;
    margin-top: 4em;
    counter-reset: page 0;
}

.title-page + * {
    counter-increment: page;
}

.title-page h1 {
    font-size: 36pt;
    font-weight: bold;
    color: #EE312E;
    margin-top: 0;
    margin-bottom: 1em;
    border-bottom: none;
    padding-bottom: 0;
}

.title-page .subtitle {
    font-size: 18pt;
    color: #D3222A;
    margin-bottom: 3em;
    font-style: italic;
}

.title-page .author {
    font-size: 14pt;
    color: #AF292B;
    margin-bottom: 1em;
}

.title-page .date {
    font-size: 12pt;
    color: #666;
    margin-bottom: 2em;
}

.letterhead {
    position: fixed;
    top: 1cm;
    right: 1cm;
    width: 3cm;
    height: auto;
    z-index: 1000;
}

.page-break {
    page-break-before: always;
}

p {
    margin-bottom: 1em;
    text-align: justify;
}

ul {
    list-style-type: disc;
    margin-bottom: 1em;
    padding-left: 2em;
}

li {
    margin-bottom: 0.5em;
}
"""

    return markdown_content, css_content

def test_logo_and_metadata():
    """Test the logo and metadata functionality."""
    
    print("Testing Borel logo and metadata fixes...")
    
    # Create test files
    markdown_content, css_content = create_test_files()
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        # Create test markdown file
        md_file = temp_dir_path / "test.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Create a simple test logo (SVG)
        logo_file = temp_dir_path / "test-logo.svg"
        logo_svg = """<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="100" fill="#EE312E"/>
  <text x="50" y="60" text-anchor="middle" fill="white" font-family="Arial" font-size="12">LOGO</text>
</svg>"""
        with open(logo_file, 'w') as f:
            f.write(logo_svg)
        
        # Process markdown
        processor = MarkdownProcessor()
        content, metadata = processor.process_file(str(md_file))
        
        print(f"Extracted metadata: {metadata}")
        
        # Generate HTML
        html_generator = HTMLGenerator()
        html_content = html_generator.generate_html(
            content, metadata, css_content, str(logo_file)
        )
        
        # Save HTML for inspection
        html_file = temp_dir_path / "test.html"
        html_generator.save_html(html_content, str(html_file))
        
        print(f"Generated HTML file: {html_file}")
        print(f"Logo file path: {logo_file}")
        
        # Check if logo is referenced in HTML
        if 'test-logo.svg' in html_content:
            print("✅ Logo is properly referenced in HTML")
        else:
            print("❌ Logo is not referenced in HTML")
        
        # Check if metadata is in HTML
        if 'Test Document with Logo and Metadata' in html_content:
            print("✅ Title metadata is in HTML")
        else:
            print("❌ Title metadata is missing from HTML")
        
        if 'Diligent Corporation' in html_content:
            print("✅ Company metadata is in HTML")
        else:
            print("❌ Company metadata is missing from HTML")
        
        if 'David Balogh' in html_content:
            print("✅ Author metadata is in HTML")
        else:
            print("❌ Author metadata is missing from HTML")
        
        print(f"\nHTML file saved to: {html_file}")
        print("You can open this file in a browser to see the result.")
        print("To generate PDF, run: python -m borel.cli {md_file} --logo {logo_file}")

if __name__ == "__main__":
    test_logo_and_metadata() 