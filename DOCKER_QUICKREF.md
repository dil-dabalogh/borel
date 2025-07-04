# Borel Docker Quick Reference

## Quick Start

```bash
# Build image
./scripts/borel-docker.sh --build

# Convert markdown to PDF
./scripts/borel-docker.sh input.md
```

## Common Commands

### Basic Usage
```bash
./scripts/borel-docker.sh input.md                    # Convert to PDF
./scripts/borel-docker.sh --help                      # Show help
./scripts/borel-docker.sh --verbose input.md          # Verbose output
```

### Custom Styling
```bash
./scripts/borel-docker.sh --css style.css input.md    # Custom CSS
./scripts/borel-docker.sh --logo logo.png input.md    # Company logo
./scripts/borel-docker.sh --company "Acme Corp" input.md  # Company name
```

### Output Control
```bash
./scripts/borel-docker.sh --output report.pdf input.md  # Specify output
./scripts/borel-docker.sh --keep-html input.md         # Keep HTML file
```

### Docker Management
```bash
./scripts/borel-docker.sh --build                     # Build/rebuild image
./scripts/borel-docker.sh --clean                     # Clean containers
./scripts/borel-docker.sh --shell                     # Interactive shell
```

## Direct Docker Commands

```bash
# Build image
docker build -t borel:latest .

# Run borel
docker run --rm -v "$(pwd):/workspace" -w /workspace borel:latest input.md

# Interactive shell
docker run --rm -it -v "$(pwd):/workspace" -w /workspace borel:latest /bin/bash
```

## Docker Compose

```bash
# Build and run
docker-compose build
docker-compose run --rm borel input.md

# Interactive mode
docker-compose run --rm borel /bin/bash
```

## Zsh Integration

Add to `~/.zshrc`:
```bash
source /path/to/borel/scripts/borel-docker.zsh
```

Then use:
```bash
borel input.md              # Run borel
borel-status               # Check Docker status
borel-build                # Build image
borel-clean                # Clean containers
borel-shell                # Interactive shell
```

## File System Mapping

- **Current directory** → `/workspace` (read/write)
- **~/.borel/** → `/home/borel/.borel` (read-only)

## Configuration

Create `borel.config.json`:
```json
{
  "css_file": "company-branding.css",
  "logo_file": "company-logo.png",
  "company_name": "Your Company",
  "default_author": "Your Name"
}
```

## Troubleshooting

```bash
# Check Docker status
docker info

# Check image exists
docker images | grep borel

# Clean up everything
docker system prune -f

# Rebuild from scratch
docker rmi borel:latest
./scripts/borel-docker.sh --build
```

## Testing

```bash
# Test Docker setup
python3 test_docker.py

# Test with sample
./scripts/borel-docker.sh examples/sample.md
```

## Performance Tips

- First run builds the image (takes time)
- Subsequent runs are fast
- Use volume mounting for file access
- Keep configuration in `~/.borel/`

## Security Notes

- Container runs as non-root user
- Configuration directory is read-only
- Minimal base image reduces attack surface 