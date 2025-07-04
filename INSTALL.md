# Borel Installation Guide

This guide will help you install Borel and all its dependencies on your system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/borel.git
cd borel
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### macOS

```bash
# Install pandoc using Homebrew
brew install pandoc

# Install WeasyPrint dependencies (if needed)
brew install cairo pango gdk-pixbuf libffi
```

#### Ubuntu/Debian

```bash
# Install pandoc
sudo apt-get update
sudo apt-get install pandoc

# Install WeasyPrint dependencies
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

#### CentOS/RHEL/Fedora

```bash
# Install pandoc
sudo yum install pandoc  # or sudo dnf install pandoc on Fedora

# Install WeasyPrint dependencies
sudo yum install gcc python3-devel cairo-devel pango-devel gdk-pixbuf2-devel libffi-devel
```

#### Windows

1. Install pandoc from [pandoc.org](https://pandoc.org/installing.html)
2. Install WeasyPrint dependencies using the Windows installer

### 4. Install Borel

```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### 5. Verify Installation

Run the test script to verify everything is working:

```bash
python test_installation.py
```

You should see all tests passing with ✅ marks.

### 6. Set Up Zsh Integration (Optional)

Add the following line to your `~/.zshrc` file:

```bash
source /path/to/borel/scripts/borel.zsh
```

Replace `/path/to/borel` with the actual path to your Borel installation.

Then reload your shell:

```bash
source ~/.zshrc
```

## Usage

### Basic Usage

```bash
# Convert a markdown file to PDF
borel input.md

# This will generate input.pdf in the same directory
```

### With Custom Branding

```bash
# Use custom CSS and logo
borel --css company-branding.css --logo company-logo.png input.md

# Specify company name and author
borel --company "Acme Corp" --author "John Doe" input.md
```

### Configuration File

Create a `borel.config.json` file in your project directory:

```json
{
  "css_file": "company-branding.css",
  "logo_file": "company-logo.png",
  "company_name": "Your Company Name",
  "default_author": "Your Name"
}
```

## Troubleshooting

### Common Issues

#### 1. WeasyPrint Installation Issues

If you encounter issues installing WeasyPrint:

```bash
# On macOS, try installing with specific flags
pip install weasyprint --no-binary :all:

# On Linux, ensure you have the required system libraries
sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev
```

#### 2. Pandoc Not Found

If pandoc is not found:

```bash
# Check if pandoc is installed
which pandoc

# If not found, install it according to your platform
# macOS: brew install pandoc
# Ubuntu: sudo apt-get install pandoc
# Windows: Download from pandoc.org
```

#### 3. Permission Issues

If you encounter permission issues:

```bash
# Use a virtual environment
python -m venv borel-env
source borel-env/bin/activate  # On Windows: borel-env\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

#### 4. Import Errors

If you see import errors for dependencies:

```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### Getting Help

If you continue to have issues:

1. Check the test script output: `python test_installation.py`
2. Verify your Python version: `python --version`
3. Check if all dependencies are installed: `pip list`
4. Look for error messages in the console output

## Development Setup

For developers who want to contribute to Borel:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run tests
python -m pytest tests/

# Format code
black borel/

# Lint code
flake8 borel/
```

## Platform-Specific Notes

### macOS

- WeasyPrint works best with Homebrew-installed dependencies
- Use `brew install` for system dependencies when possible

### Linux

- Different distributions may require different package names
- Check your distribution's package manager for the correct package names

### Windows

- Consider using WSL (Windows Subsystem for Linux) for easier installation
- Ensure all system dependencies are properly installed
- Use the Windows installer for WeasyPrint if available

## Next Steps

After successful installation:

1. Try the sample file: `borel examples/sample.md`
2. Create your own markdown file and convert it
3. Customize the CSS styling for your company branding
4. Set up your configuration file for consistent formatting

For more information, see the main [README.md](README.md) file. 