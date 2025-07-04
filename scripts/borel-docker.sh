#!/bin/bash
#
# Borel Docker wrapper script
# This script makes it easy to run Borel in a Docker container
# Usage: ./borel-docker.sh [borel-arguments]
#

set -e

# Configuration
IMAGE_NAME="borel:latest"
CONTAINER_NAME="borel-cli"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the Docker image if it doesn't exist
build_image() {
    if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
        print_info "Building Borel Docker image..."
        docker build -t "$IMAGE_NAME" "$PROJECT_ROOT"
        print_success "Docker image built successfully!"
    else
        print_info "Docker image already exists."
    fi
}

# Function to clean up old containers
cleanup_containers() {
    if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_info "Cleaning up old container..."
        docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
}

# Function to run borel in Docker
run_borel() {
    local args="$*"
    
    # If no arguments provided, show help
    if [ -z "$args" ]; then
        args="--help"
    fi
    
    # Create .borel directory in user's home if it doesn't exist
    mkdir -p ~/.borel
    
    # Run the container
    docker run --rm \
        --name "$CONTAINER_NAME" \
        -v "$(pwd):/workspace" \
        -v "$HOME/.borel:/home/borel/.borel:ro" \
        -w /workspace \
        -e PYTHONPATH=/app \
        "$IMAGE_NAME" \
        $args
}

# Function to show usage
show_usage() {
    echo "Borel Docker Wrapper"
    echo ""
    echo "Usage: $0 [borel-arguments]"
    echo ""
    echo "Examples:"
    echo "  $0 --help                    # Show borel help"
    echo "  $0 input.md                  # Convert markdown to PDF"
    echo "  $0 --css style.css input.md  # Use custom CSS"
    echo "  $0 --verbose input.md        # Verbose output"
    echo ""
    echo "Docker Commands:"
    echo "  $0 --build                   # Rebuild Docker image"
    echo "  $0 --clean                   # Clean up containers"
    echo "  $0 --shell                   # Run interactive shell"
    echo ""
    echo "The current directory is mounted to /workspace in the container."
    echo "Configuration files can be placed in ~/.borel/"
}

# Function to run interactive shell
run_shell() {
    print_info "Starting interactive shell in Borel container..."
    docker run --rm -it \
        --name "${CONTAINER_NAME}-shell" \
        -v "$(pwd):/workspace" \
        -v "$HOME/.borel:/home/borel/.borel:ro" \
        -w /workspace \
        -e PYTHONPATH=/app \
        "$IMAGE_NAME" \
        /bin/bash
}

# Main script logic
main() {
    # Check if Docker is available
    check_docker
    
    # Handle special commands
    case "${1:-}" in
        --help|-h)
            show_usage
            exit 0
            ;;
        --build)
            print_info "Building Docker image..."
            docker build -t "$IMAGE_NAME" "$PROJECT_ROOT"
            print_success "Docker image built successfully!"
            exit 0
            ;;
        --clean)
            cleanup_containers
            print_success "Cleanup completed!"
            exit 0
            ;;
        --shell)
            build_image
            run_shell
            exit 0
            ;;
    esac
    
    # Build image if needed
    build_image
    
    # Clean up old containers
    cleanup_containers
    
    # Run borel with provided arguments
    run_borel "$@"
}

# Run main function with all arguments
main "$@" 