#!/bin/bash
# =============================================================================
# Secret Detection Script for Zscaler SDK Python
# =============================================================================
# This script scans the codebase for potential secret leakages using
# industry-standard tools: detect-secrets and trufflehog.
#
# Usage: ./scripts/check-secrets.sh [options]
#
# Options:
#   --cassettes-only    Only scan VCR cassettes
#   --full              Scan entire repository (excluding .gitignore paths)
#   --install           Install required tools
#   --help              Show this help message
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default paths to scan
CASSETTES_PATH="tests/integration/*/cassettes/"
ADDITIONAL_SCAN_PATHS="docs docsrc examples"
EXCLUDE_PATHS="local_dev,*.pyc,__pycache__,.git,.venv,*.egg-info"

# Functions
print_header() {
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}   $1${NC}"
    echo -e "${BLUE}=========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_tool() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

install_tools() {
    print_header "Installing Secret Detection Tools"
    
    echo "Installing detect-secrets..."
    pip install detect-secrets 2>&1 | tail -3
    
    echo ""
    echo "Installing trufflehog..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install trufflehog 2>&1 | tail -3 || pip install trufflehog
    else
        pip install trufflehog 2>&1 | tail -3
    fi
    
    print_success "Tools installed successfully!"
}

scan_with_detect_secrets() {
    local scan_path="$1"
    echo ""
    echo -e "${YELLOW}--- Running detect-secrets ---${NC}"
    
    if ! check_tool "python"; then
        print_error "Python not found. Please install Python first."
        return 1
    fi
    
    local result
    local baseline_arg=""
    
    # Use baseline file if it exists to filter known false positives
    if [[ -f "$PROJECT_ROOT/.secrets.baseline" ]]; then
        # Compare against baseline - only show NEW secrets
        result=$(python -m detect_secrets scan "$scan_path" 2>&1)
        # Filter out secrets that are in the baseline
        local new_secrets
        new_secrets=$(echo "$result" | python3 -c "
import sys, json
try:
    # Load scan results
    scan_data = json.load(sys.stdin)
    scan_results = scan_data.get('results', {})
    
    # Load baseline
    try:
        with open('$PROJECT_ROOT/.secrets.baseline', 'r') as f:
            baseline_data = json.load(f)
        baseline_results = baseline_data.get('results', {})
    except:
        baseline_results = {}
    
    # Find new secrets not in baseline
    new_results = {}
    for filepath, secrets in scan_results.items():
        baseline_secrets = baseline_results.get(filepath, [])
        baseline_hashes = {s.get('hashed_secret') for s in baseline_secrets}
        new_secrets_for_file = [s for s in secrets if s.get('hashed_secret') not in baseline_hashes]
        if new_secrets_for_file:
            new_results[filepath] = new_secrets_for_file
    
    # Output new results
    scan_data['results'] = new_results
    print(json.dumps(scan_data))
except Exception as e:
    print(json.dumps({'results': {}, 'error': str(e)}))
" 2>/dev/null)
        result="$new_secrets"
    else
        result=$(python -m detect_secrets scan "$scan_path" 2>&1)
    fi
    
    local secrets_found
    secrets_found=$(echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', {})
    if not results:
        print('0')
    else:
        count = sum(len(v) for v in results.values())
        print(count)
except:
    print('error')
" 2>/dev/null)
    
    if [[ "$secrets_found" == "0" ]]; then
        print_success "detect-secrets: No secrets found"
        return 0
    elif [[ "$secrets_found" == "error" ]]; then
        print_warning "detect-secrets: Could not parse results"
        return 1
    else
        print_error "detect-secrets: Found $secrets_found potential secret(s)!"
        echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for filepath, secrets in data.get('results', {}).items():
    print(f'\n  📁 {filepath}:')
    for secret in secrets:
        print(f'     Line {secret[\"line_number\"]}: {secret[\"type\"]}')
"
        return 1
    fi
}

scan_with_trufflehog() {
    local scan_path="$1"
    echo ""
    echo -e "${YELLOW}--- Running trufflehog ---${NC}"
    
    if ! check_tool "trufflehog"; then
        print_warning "trufflehog not found. Skipping..."
        return 0
    fi
    
    local result
    result=$(trufflehog filesystem "$scan_path" --no-update 2>&1)
    
    local verified_secrets
    local unverified_secrets
    verified_secrets=$(echo "$result" | grep -o '"verified_secrets": [0-9]*' | grep -o '[0-9]*' || echo "0")
    unverified_secrets=$(echo "$result" | grep -o '"unverified_secrets": [0-9]*' | grep -o '[0-9]*' || echo "0")
    
    if [[ "$verified_secrets" == "0" && "$unverified_secrets" == "0" ]]; then
        print_success "trufflehog: No secrets found"
        return 0
    else
        if [[ "$verified_secrets" != "0" ]]; then
            print_error "trufflehog: Found $verified_secrets VERIFIED secret(s)!"
        fi
        if [[ "$unverified_secrets" != "0" ]]; then
            print_warning "trufflehog: Found $unverified_secrets unverified potential secret(s)"
        fi
        echo "$result" | grep -A5 "Found" | head -50
        return 1
    fi
}

scan_cassettes() {
    print_header "Scanning VCR Cassettes & Documentation for Secrets"
    
    cd "$PROJECT_ROOT"
    
    local cassette_count
    cassette_count=$(find tests/integration/*/cassettes -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
    echo "Found $cassette_count cassette files to scan"
    echo "Also scanning: $ADDITIONAL_SCAN_PATHS"
    echo ""
    
    local exit_code=0
    
    # Scan cassettes
    echo -e "${YELLOW}=== Scanning VCR Cassettes ===${NC}"
    scan_with_detect_secrets "$CASSETTES_PATH" || exit_code=1
    scan_with_trufflehog "$CASSETTES_PATH" || exit_code=1
    
    # Scan additional paths (docs, docsrc, examples)
    for path in $ADDITIONAL_SCAN_PATHS; do
        if [[ -d "$path" ]]; then
            echo ""
            echo -e "${YELLOW}=== Scanning $path ===${NC}"
            scan_with_detect_secrets "$path" || exit_code=1
            scan_with_trufflehog "$path" || exit_code=1
        fi
    done
    
    return $exit_code
}

scan_full() {
    print_header "Full Repository Scan for Secrets"
    
    cd "$PROJECT_ROOT"
    
    echo "Scanning entire repository (excluding: $EXCLUDE_PATHS)"
    echo ""
    
    local exit_code=0
    
    # Create temp file with exclusions
    local exclude_args=""
    IFS=',' read -ra PATHS <<< "$EXCLUDE_PATHS"
    for path in "${PATHS[@]}"; do
        exclude_args="$exclude_args --exclude-dir=$path"
    done
    
    scan_with_detect_secrets "." || exit_code=1
    
    # For trufflehog, use --exclude-paths
    echo ""
    echo -e "${YELLOW}--- Running trufflehog (excluding local_dev) ---${NC}"
    if check_tool "trufflehog"; then
        trufflehog filesystem . --no-update --exclude-paths="local_dev" 2>&1 | tail -5
    fi
    
    return $exit_code
}

show_help() {
    echo "Secret Detection Script for Zscaler SDK Python"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --cassettes-only    Only scan VCR cassettes (default)"
    echo "  --full              Scan entire repository"
    echo "  --install           Install required tools"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                  # Scan cassettes only"
    echo "  $0 --full           # Scan entire repository"
    echo "  $0 --install        # Install detect-secrets and trufflehog"
}

# Main
main() {
    local mode="cassettes"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --cassettes-only)
                mode="cassettes"
                shift
                ;;
            --full)
                mode="full"
                shift
                ;;
            --install)
                install_tools
                exit 0
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo ""
    print_header "Secret Detection Scan"
    echo "Mode: $mode"
    echo "Project: $PROJECT_ROOT"
    echo ""
    
    local exit_code=0
    
    case $mode in
        cassettes)
            scan_cassettes || exit_code=1
            ;;
        full)
            scan_full || exit_code=1
            ;;
    esac
    
    echo ""
    if [[ $exit_code -eq 0 ]]; then
        print_header "SCAN COMPLETE - ALL CLEAR"
        print_success "No secrets detected. Safe to commit!"
    else
        print_header "SCAN COMPLETE - ISSUES FOUND"
        print_error "Potential secrets detected. Please review and fix before committing."
    fi
    
    exit $exit_code
}

main "$@"

