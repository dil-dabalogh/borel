# Borel Docker Guide

This guide explains how to use Borel in a Docker container, which provides a consistent environment across different systems and eliminates the need to install dependencies locally.

## Prerequisites

- **Docker Desktop** for macOS (or Docker Engine for Linux)
- Git (for cloning the repository)

## Quick Start

### 1. Clone and Build

```bash
git clone https://github.com/your-org/borel.git
cd borel

# Build the Docker image
./scripts/borel-docker.sh --build
```

### 2. Convert Your First Document

```bash
# Convert a markdown file to PDF
./scripts/borel-docker.sh examples/sample.md

# This will generate examples/sample.pdf
```

## Installation Options

### Option 1: Using the Docker Wrapper Script (Recommended)

The easiest way to use Borel with Docker is through the provided wrapper script:

```bash
# Make the script executable (if not already)
chmod +x scripts/borel-docker.sh

# Use borel commands
./scripts/borel-docker.sh input.md
./scripts/borel-docker.sh --css style.css input.md
./scripts/borel-docker.sh --verbose input.md
```

### Option 2: Direct Docker Commands

You can also run Docker commands directly:

```bash
# Build the image
docker build -t borel:latest .

# Run borel
docker run --rm -v "$(pwd):/workspace" -w /workspace borel:latest input.md
```

### Option 3: Docker Compose

For development and testing:

```bash
# Build and run with docker-compose
docker-compose build
docker-compose run --rm borel input.md
```

### Option 4: Zsh Integration

Add Docker integration to your shell:

```bash
# Add to your ~/.zshrc
source /path/to/borel/scripts/borel-docker.zsh

# Reload shell
source ~/.zshrc

# Now you can use borel directly
borel input.md
borel-status  # Check Docker status
borel-build   # Build Docker image
```

## Usage Examples

### Basic Usage

```bash
# Convert markdown to PDF
./scripts/borel-docker.sh document.md

# Use custom CSS
./scripts/borel-docker.sh --css company-branding.css document.md

# Specify output file
./scripts/borel-docker.sh --output report.pdf document.md

# Verbose output
./scripts/borel-docker.sh --verbose document.md
```

### With Company Branding

```bash
# Use custom CSS and logo
./scripts/borel-docker.sh \
  --css company-branding.css \
  --logo company-logo.png \
  --company "Acme Corporation" \
  document.md
```

### Configuration File

Create a `borel.config.json` in your project directory:

```json
{
  "css_file": "company-branding.css",
  "logo_file": "company-logo.png",
  "company_name": "Your Company",
  "default_author": "Your Name"
}
```

The Docker container will automatically use this configuration.

## Docker Commands

The wrapper script provides several Docker-specific commands:

```bash
# Show help
./scripts/borel-docker.sh --help

# Build/rebuild Docker image
./scripts/borel-docker.sh --build

# Clean up containers
./scripts/borel-docker.sh --clean

# Run interactive shell in container
./scripts/borel-docker.sh --shell
```

## File System Mapping

The Docker container maps your local filesystem:

- **Current directory** → `/workspace` (read/write)
- **Home directory** → `/home/borel/.borel` (read-only for config)

This means:
- Input files should be in your current directory
- Output PDFs will appear in your current directory
- Configuration files can be placed in `~/.borel/`

## Development Workflow

### Interactive Development

```bash
# Start an interactive shell in the container
./scripts/borel-docker.sh --shell

# Inside the container, you can:
borel --help
borel input.md
python -c "import borel; print('Module works!')"
```

### Testing Changes

```bash
# Rebuild after code changes
./scripts/borel-docker.sh --build

# Test with sample file
./scripts/borel-docker.sh examples/sample.md
```

## Troubleshooting

### Common Issues

#### 1. Docker Not Running

```bash
# Check Docker status
docker info

# Start Docker Desktop (macOS)
open -a Docker
```

#### 2. Permission Issues

```bash
# Make script executable
chmod +x scripts/borel-docker.sh

# Check file permissions
ls -la scripts/borel-docker.sh
```

#### 3. Image Build Failures

```bash
# Clean up and rebuild
docker system prune -f
./scripts/borel-docker.sh --build
```

#### 4. File Not Found

Ensure your files are in the current directory:

```bash
# Check current directory contents
ls -la

# Run from the correct directory
cd /path/to/your/documents
./scripts/borel-docker.sh document.md
```

#### 5. Font Issues

If you encounter font rendering issues:

```bash
# Rebuild with additional fonts
docker build --build-arg ADD_FONTS=true -t borel:latest .
```

### Debugging

#### Enable Verbose Output

```bash
./scripts/borel-docker.sh --verbose input.md
```

#### Check Container Logs

```bash
# Run with explicit container name
docker run --name borel-debug -v "$(pwd):/workspace" borel:latest input.md

# Check logs
docker logs borel-debug

# Clean up
docker rm borel-debug
```

#### Interactive Debugging

```bash
# Start container with bash
docker run --rm -it -v "$(pwd):/workspace" -w /workspace borel:latest /bin/bash

# Inside container, run commands manually
borel --help
borel input.md
```

## Performance Optimization

### Image Size

The Docker image is optimized for size:

- Uses Python 3.11 slim base image
- Installs only necessary system dependencies
- Removes package cache after installation

### Build Caching

Docker build uses layer caching:

- Requirements are installed first for better caching
- Code changes don't trigger dependency reinstallation

### Volume Mounting

File access is optimized:

- Current directory is mounted for input/output
- Configuration directory is mounted read-only
- No file copying required

## Security Considerations

### Non-Root User

The container runs as a non-root user (`borel`) for security.

### Read-Only Configuration

The configuration directory is mounted read-only to prevent accidental modifications.

### Minimal Base Image

Uses a minimal Python slim image to reduce attack surface.

## Advanced Usage

### Custom Dockerfile

You can create a custom Dockerfile for your specific needs:

```dockerfile
FROM borel:latest

# Add custom fonts
COPY fonts/ /usr/share/fonts/custom/

# Add custom CSS
COPY custom-styles.css /app/custom-styles.css

# Set default configuration
ENV BOREL_DEFAULT_CSS=/app/custom-styles.css
```

### Multi-Stage Build

For production deployments:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
# ... rest of runtime setup
```

### Docker Compose for Teams

Create a `docker-compose.override.yml` for team-specific settings:

```yaml
version: '3.8'
services:
  borel:
    volumes:
      - ./team-config:/home/borel/.borel
      - ./templates:/app/templates
    environment:
      - BOREL_TEAM_MODE=true
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Build and Test Borel
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t borel:latest .
      - name: Test conversion
        run: docker run --rm -v "$(pwd):/workspace" borel:latest examples/sample.md
      - name: Verify output
        run: test -f examples/sample.pdf
```

## Support

For issues specific to Docker:

1. Check Docker Desktop is running
2. Verify the image was built correctly
3. Check file permissions and paths
4. Review the troubleshooting section above

For general Borel issues, see the main [README.md](README.md) and [INSTALL.md](INSTALL.md). 