#!/bin/zsh
#
# Borel zsh integration script
# Add this to your .zshrc file to enable the borel command
#

# Function to check if borel is available
_borel_check() {
    if ! command -v borel >/dev/null 2>&1; then
        echo "Error: borel command not found. Please install the borel package first."
        echo "Install with: pip install -e ."
        return 1
    fi
}

# Main borel function
borel() {
    # Check if borel is available
    _borel_check || return 1
    
    # Call the actual borel command
    command borel "$@"
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