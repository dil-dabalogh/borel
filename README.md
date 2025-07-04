# Borel

A CLI application that parses Markdown formatted text and generates print-ready notes with company branding.

## Features

- **Markdown Processing**: Converts standard Markdown to print-ready PDF documents
- **Company Branding**: Supports custom CSS styling and company logo integration
- **Page Breaks**: Use `[CRLF]` tokens in markdown for page breaks
- **Title Page**: Automatic generation of title page with title, subtitle, author, and date
- **Letterhead**: Company logo appears in upper right corner of each page (except title page)
- **Footer**: Company name and year on each page
- **Zsh Integration**: Simple terminal command `borel filename.md` to generate `filename.pdf`

## Installation

### Option 1: Docker (Recommended)

The easiest way to use Borel is with Docker, which provides a consistent environment:

```bash
# Clone the repository
git clone https://github.com/your-org/borel.git
cd borel

# Build and use with Docker
./scripts/borel-docker.sh --build
./scripts/borel-docker.sh examples/sample.md
```

For detailed Docker instructions, see [DOCKER.md](DOCKER.md).

### Option 2: Local Installation

#### Prerequisites

- Python 3.8+
- Pandoc
- WeasyPrint

#### Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install system dependencies:
   ```bash
   # macOS
   brew install pandoc
   
   # Ubuntu/Debian
   sudo apt-get install pandoc
   ```

4. Add zsh integration to your `.zshrc`:
   ```bash
   source /path/to/borel/scripts/borel.zsh
   ```

## Usage

### Docker Usage (Recommended)

```bash
# Basic usage
./scripts/borel-docker.sh input.md

# With custom branding
./scripts/borel-docker.sh --css company-branding.css --logo company-logo.png input.md

# Verbose output
./scripts/borel-docker.sh --verbose input.md
```

### Local Usage

```bash
# Basic usage
borel input.md

# With custom branding
borel --css company-branding.css --logo company-logo.png input.md
```

### Configuration

Create a `borel.config.json` file in your project directory:

```json
{
  "css_file": "company-branding.css",
  "logo_file": "company-logo.png",
  "company_name": "Your Company Name",
  "default_author": "Your Name"
}
```

## Markdown Format

### Standard Markdown

Borel supports all standard Markdown syntax:

```markdown
# Title
## Subtitle

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2
```

### Page Breaks

Use `[CRLF]` to insert page breaks:

```markdown
# First Page Content

[CRLF]

# Second Page Content
```

### Title Page

The first page is automatically formatted as a title page. You can specify title page metadata:

```markdown
---
title: Document Title
subtitle: Document Subtitle
author: Author Name
date: 2024-01-15
---

# Main Content Starts Here
```

## Project Structure

```
borel/
├── borel/
│   ├── __init__.py
│   ├── cli.py
│   ├── processor.py
│   ├── html_generator.py
│   ├── pdf_generator.py
│   └── config.py
├── templates/
│   ├── base.html
│   └── title_page.html
├── scripts/
│   └── borel.zsh
├── requirements.txt
├── setup.py
└── README.md
```

## Development

### Running Tests

```bash
python -m pytest tests/
# Or run a specific test
python tests/test_logo.py
python tests/test_installation.py
```

### Building Distribution

```bash
python setup.py sdist bdist_wheel
```

## License

MIT License - see LICENSE file for details. 