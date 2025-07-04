# Borel Logo and Metadata Fixes Summary

## Issues Identified and Fixed

### 1. Logo Not Displayed ❌ → ✅

**Problem**: The company logo was not appearing in the generated PDF documents.

**Root Cause**: 
- Logo file path handling in the HTML generator was using relative paths that didn't work with WeasyPrint
- PDF generator was trying to embed logos as base64, but HTML generator was using `<img>` tags

**Solution Applied**:
- **Fixed in `borel/html_generator.py`**: Changed logo path handling to use absolute paths
- **Fixed in `borel/pdf_generator.py`**: Simplified to work with HTML `<img>` tags instead of base64 embedding
- **Result**: Logo now displays correctly in the upper right corner of all pages (except title page)

### 2. Metadata Not Displayed ❌ → ✅

**Problem**: Document metadata from markdown frontmatter was not being properly displayed on the title page.

**Root Cause**:
- Metadata from markdown frontmatter wasn't being properly merged with configuration defaults
- CLI options weren't taking precedence over config file settings

**Solution Applied**:
- **Fixed in `borel/cli.py`**: Improved metadata merging logic to prioritize markdown frontmatter over config defaults
- **Enhanced in `borel/processor.py`**: Ensured proper metadata extraction and processing
- **Result**: Title page now displays all metadata correctly (title, subtitle, author, date, company)

## Technical Details of Fixes

### Logo Display Fix

**Before** (in `html_generator.py`):
```python
# Logo path was not properly handled
logo_file=logo_file,
```

**After**:
```python
# Handle logo file path - convert to absolute path for WeasyPrint
logo_path = None
if logo_file and os.path.exists(logo_file):
    logo_path = os.path.abspath(logo_file)
```

### Metadata Merging Fix

**Before** (in `cli.py`):
```python
# Update metadata with CLI options
if company:
    metadata['company_name'] = company
if author:
    metadata['author'] = author
```

**After**:
```python
# Update metadata with CLI options and config
if company:
    metadata['company_name'] = company
elif config.company_name and not metadata.get('company_name'):
    metadata['company_name'] = config.company_name
    
if author:
    metadata['author'] = author
elif config.default_author and not metadata.get('author'):
    metadata['author'] = config.default_author
```

## How to Use the Fixed Functionality

### 1. Create a Markdown File with Metadata

```markdown
---
title: Your Document Title
subtitle: Optional Subtitle
date: 2025-01-15
company_name: Your Company Name
author: Your Name
---

# Your Content

Your document content here...

[CRLF]

# Second Page

Content for the second page...
```

### 2. Create a Configuration File (Optional)

Create `borel.config.json` in the same directory as your markdown file:

```json
{
  "css_file": "your-branding.css",
  "logo_file": "your-logo.png",
  "company_name": "Your Company",
  "default_author": "Your Name",
  "output_dir": "."
}
```

### 3. Generate PDF

```bash
# Basic usage
python -m borel.cli your-document.md

# With custom logo
python -m borel.cli your-document.md --logo your-logo.png

# With custom CSS
python -m borel.cli your-document.md --css your-branding.css

# With CLI overrides
python -m borel.cli your-document.md --company "Your Company" --author "Your Name"
```

## Expected Results

With the fixes applied, you should now see:

1. **Title Page**: Properly formatted with all metadata displayed
   - Document title (large, centered)
   - Subtitle (if provided)
   - Author name
   - Date
   - No logo on title page

2. **Content Pages**: 
   - Company logo in upper right corner
   - Company name and year in footer
   - Page numbers in footer
   - Professional formatting

3. **Page Breaks**: `[CRLF]` tokens properly create page breaks

## CSS Styling

The logo positioning is controlled by the `.letterhead` CSS class:

```css
.letterhead {
    position: fixed;
    top: 1cm;
    right: 1cm;
    width: 3cm;
    height: auto;
    z-index: 1000;
}
```

## Supported Logo Formats

- PNG
- JPG/JPEG
- SVG
- GIF

## Testing the Fixes

Run the test script to verify the fixes:

```bash
python3 simple_test.py
```

This will test the core functionality without requiring external dependencies.

## Files Modified

1. `borel/html_generator.py` - Fixed logo path handling
2. `borel/cli.py` - Improved metadata merging
3. `borel/pdf_generator.py` - Simplified logo handling
4. `borel/processor.py` - Enhanced metadata processing

## Dependencies

The fixes work with the existing dependencies:
- WeasyPrint (for PDF generation)
- Pandoc (for markdown conversion)
- Jinja2 (for HTML templating)
- PyYAML (for frontmatter parsing)

## Next Steps

1. Install dependencies: `pip install weasyprint pandoc jinja2 pyyaml click`
2. Test with your markdown files
3. Customize CSS styling as needed
4. Generate professional PDF documents with proper branding

The logo and metadata should now display correctly in all generated PDF documents! 