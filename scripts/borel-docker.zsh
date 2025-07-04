#!/bin/zsh
#
# Borel Docker zsh integration script
# Add this to your .zshrc file to enable the borel command with Docker
#

# Function to check if Docker is available
_borel_docker_check() {
    if ! command -v docker >/dev/null 2>&1; then
        echo "Error: Docker is not installed or not in PATH."
        echo "Please install Docker Desktop for macOS."
        return 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        echo "Error: Docker is not running. Please start Docker Desktop."
        return 1
    fi
}

# Function to get the borel-docker.sh script path
_borel_get_script_path() {
    # Try to find the script in common locations
    local script_paths=(
        "$(pwd)/scripts/borel-docker.sh"
        "$(dirname "$0")/borel-docker.sh"
        "$HOME/.borel/borel-docker.sh"
        "/usr/local/bin/borel-docker.sh"
    )
    
    for path in "${script_paths[@]}"; do
        if [[ -f "$path" && -x "$path" ]]; then
            echo "$path"
            return 0
        fi
    done
    
    echo "Error: borel-docker.sh script not found."
    echo "Please ensure the script is in your PATH or current directory."
    return 1
}

# Main borel function for Docker
borel() {
    # Check if Docker is available
    _borel_docker_check || return 1
    
    # Get the script path
    local script_path
    script_path=$(_borel_get_script_path) || return 1
    
    # Run the Docker wrapper script
    "$script_path" "$@"
}

# Completion function for borel
_borel_completion() {
    local curcontext="$curcontext" state line
    typeset -A opt_args

    _arguments -C \
        '1: :->cmds' \
        '*:: :->args'

    case "$state" in
        cmds)
            _files -g "*.md"
            ;;
        args)
            case $line[1] in
                --css|-c)
                    _files -g "*.css"
                    ;;
                --logo|-l)
                    _files -g "*.{png,jpg,jpeg,gif,svg}"
                    ;;
                --output|-o)
                    _files -g "*.pdf"
                    ;;
                *)
                    _files
                    ;;
            esac
            ;;
    esac
}

# Register completion function
compdef _borel_completion borel

# Export function for use in scripts
export -f borel

# Function to show Docker status
borel-status() {
    echo "Borel Docker Status:"
    echo "==================="
    
    if command -v docker >/dev/null 2>&1; then
        echo "✅ Docker is installed"
        
        if docker info >/dev/null 2>&1; then
            echo "✅ Docker is running"
            
            if docker image inspect borel:latest >/dev/null 2>&1; then
                echo "✅ Borel Docker image exists"
            else
                echo "❌ Borel Docker image not found"
                echo "   Run: borel --build"
            fi
        else
            echo "❌ Docker is not running"
        fi
    else
        echo "❌ Docker is not installed"
    fi
}

# Function to build the Docker image
borel-build() {
    local script_path
    script_path=$(_borel_get_script_path) || return 1
    "$script_path" --build
}

# Function to clean up containers
borel-clean() {
    local script_path
    script_path=$(_borel_get_script_path) || return 1
    "$script_path" --clean
}

# Function to run interactive shell
borel-shell() {
    local script_path
    script_path=$(_borel_get_script_path) || return 1
    "$script_path" --shell
} 