# Borel Quick Start Guide

Get up and running with Borel in 5 minutes!

## Prerequisites

- Python 3.8+
- pip

## Quick Installation

1. **Install dependencies:**
   ```bash
   pip install click pypandoc weasyprint jinja2 pyyaml
   ```

2. **Install pandoc:**
   ```bash
   # macOS
   brew install pandoc
   
   # Ubuntu/Debian
   sudo apt-get install pandoc
   ```

3. **Install Borel:**
   ```bash
   pip install -e .
   ```

## Your First Document

1. **Create a markdown file** (`my-document.md`):
   ```markdown
   ---
   title: My First Document
   subtitle: Created with Borel
   author: Your Name
   date: 2024-01-15
   ---
   
   # Introduction
   
   This is my first document created with Borel!
   
   ## Features
   
   - Professional formatting
   - Company branding
   - Page breaks with [CRLF]
   
   [CRLF]
   
   # Second Page
   
   This content appears on the second page.
   ```

2. **Generate PDF:**
   ```bash
   borel my-document.md
   ```

3. **View your PDF!** The file `my-document.pdf` will be created in the same directory.

## Try the Sample

Test with the included sample:

```bash
borel examples/sample.md
```

This will generate `examples/sample.pdf` with professional formatting.

## Custom Branding

1. **Create a CSS file** (`my-branding.css`):
   ```css
   body {
       font-family: 'Arial', sans-serif;
       color: #333;
   }
   
   h1 {
       color: #2c3e50;
       border-bottom: 2pt solid #3498db;
   }
   ```

2. **Use with your document:**
   ```bash
   borel --css my-branding.css my-document.md
   ```

## Configuration File

Create `borel.config.json` in your project directory:

```json
{
  "css_file": "my-branding.css",
  "logo_file": "company-logo.png",
  "company_name": "My Company",
  "default_author": "Your Name"
}
```

## Page Breaks

Use `[CRLF]` in your markdown to create page breaks:

```markdown
# First Page Content

[CRLF]

# Second Page Content
```

## Command Line Options

```bash
# Basic usage
borel input.md

# With custom styling
borel --css style.css --logo logo.png input.md

# Specify output file
borel --output report.pdf input.md

# Keep intermediate HTML
borel --keep-html input.md

# Verbose output
borel --verbose input.md
```

## Zsh Integration

Add to your `~/.zshrc`:

```bash
source /path/to/borel/scripts/borel.zsh
```

Then use tab completion: `borel <TAB>`

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [INSTALL.md](INSTALL.md) for troubleshooting
- Customize the CSS for your company branding
- Create templates for different document types

## Need Help?

Run the test script to check your installation:

```bash
python tests/test_installation.py
```

This will verify all dependencies are properly installed. 