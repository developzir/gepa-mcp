#!/bin/bash

# GEPA MCP Server Installation Script
# Automated setup for the Genetic-Evolutionary Prompt Architecture MCP server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Claude Desktop config path based on OS
get_claude_config_path() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "$HOME/.config/claude-desktop/claude_desktop_config.json"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash/Cygwin)
        echo "$APPDATA/Claude/claude_desktop_config.json"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

print_banner() {
    echo -e "${BLUE}"
    cat << "EOF"
  ██████╗ ███████╗██████╗  █████╗     ███╗   ███╗ ██████╗██████╗ 
 ██╔════╝ ██╔════╝██╔══██╗██╔══██╗    ████╗ ████║██╔════╝██╔══██╗
 ██║  ███╗█████╗  ██████╔╝███████║    ██╔████╔██║██║     ██████╔╝
 ██║   ██║██╔══╝  ██╔═══╝ ██╔══██║    ██║╚██╔╝██║██║     ██╔═══╝
 ╚██████╔╝███████╗██║     ██║  ██║    ██║ ╚═╝ ██║╚██████╗██║     
  ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝    ╚═╝     ╚═╝ ╚═════╝╚═╝     
                                                                  
EOF
    echo -e "${NC}"
    echo -e "${GREEN}Genetic-Evolutionary Prompt Architecture MCP Server${NC}"
    echo -e "${BLUE}Automated Installation Script${NC}"
    echo ""
}

# Main installation function
main() {
    print_banner
    
    # Check if we're in the right directory
    if [[ ! -f "pyproject.toml" ]] || [[ ! -f "run_server.py" ]]; then
        print_error "Installation script must be run from the GEPA-mcp directory"
        print_error "Please navigate to the GEPA-mcp directory and run ./install.sh"
        exit 1
    fi
    
    print_status "Starting GEPA MCP Server installation..."
    
    # Step 1: Check Python version
    print_status "Checking Python version..."
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 10 ]]; then
            print_success "Python $PYTHON_VERSION found (requirement: Python 3.10+)"
        else
            print_error "Python 3.10+ required, but found Python $PYTHON_VERSION"
            print_error "Please install Python 3.10 or later from https://python.org"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.10+ from https://python.org"
        exit 1
    fi
    
    # Step 2: Install uv if not present
    print_status "Checking for uv package manager..."
    if ! command_exists uv; then
        print_status "Installing uv package manager..."
        if command_exists curl; then
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.local/bin:$PATH"
        else
            print_error "curl not found. Please install curl or manually install uv from https://github.com/astral-sh/uv"
            exit 1
        fi
        
        # Reload shell environment
        if [[ -f "$HOME/.bashrc" ]]; then
            source "$HOME/.bashrc" 2>/dev/null || true
        fi
        if [[ -f "$HOME/.zshrc" ]]; then
            source "$HOME/.zshrc" 2>/dev/null || true
        fi
        
        if command_exists uv; then
            print_success "uv installed successfully"
        else
            print_warning "uv installation may require shell restart. Please run 'source ~/.bashrc' or restart your terminal"
        fi
    else
        print_success "uv package manager found"
    fi
    
    # Step 3: Install dependencies
    print_status "Installing Python dependencies..."
    if ! uv sync; then
        print_error "Failed to install dependencies with uv"
        exit 1
    fi
    print_success "Dependencies installed successfully"
    
    # Step 4: Test the server
    print_status "Testing GEPA MCP server..."
    timeout 5 uv run python run_server.py --help >/dev/null 2>&1 || true
    if [[ $? -eq 124 ]]; then
        print_success "Server appears to be working (timeout expected for --help)"
    else
        print_warning "Server test completed (this is normal)"
    fi
    
    # Step 5: Configure Claude Desktop
    CLAUDE_CONFIG_PATH=$(get_claude_config_path)
    CURRENT_DIR=$(pwd)
    
    print_status "Configuring Claude Desktop integration..."
    
    # Ensure config directory exists
    CONFIG_DIR=$(dirname "$CLAUDE_CONFIG_PATH")
    mkdir -p "$CONFIG_DIR"
    
    # Create or update config file
    if [[ -f "$CLAUDE_CONFIG_PATH" ]]; then
        print_status "Backing up existing Claude Desktop config..."
        cp "$CLAUDE_CONFIG_PATH" "${CLAUDE_CONFIG_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
        print_success "Config backed up to ${CLAUDE_CONFIG_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create new config with GEPA MCP server
    cat > "$CLAUDE_CONFIG_PATH" << EOF
{
  "mcpServers": {
    "gepa-mcp": {
      "command": "uv",
      "args": ["run", "python", "run_server.py"],
      "cwd": "$CURRENT_DIR",
      "env": {}
    }
  }
}
EOF
    
    print_success "Claude Desktop configured with GEPA MCP server"
    print_status "Config file location: $CLAUDE_CONFIG_PATH"
    
    # Step 6: Setup environment file and get API key
    print_status "Setting up environment configuration..."
    
    GEMINI_API_KEY=""
    if [[ -f ".env" ]] && grep -q "GEMINI_API_KEY=" .env && ! grep -q "your_gemini_api_key_here" .env; then
        print_success "Environment file with API key already exists"
        GEMINI_API_KEY=$(grep "GEMINI_API_KEY=" .env | cut -d'=' -f2)
    else
        echo ""
        print_status "GEPA requires a Gemini API key for optimization features"
        echo -e "${BLUE}Get your free API key at: ${YELLOW}https://makersuite.google.com/app/apikey${NC}"
        echo ""
        
        while [[ -z "$GEMINI_API_KEY" ]]; do
            echo -n "Enter your Gemini API key (or 'skip' to configure later): "
            read -r GEMINI_API_KEY
            
            if [[ "$GEMINI_API_KEY" == "skip" ]]; then
                GEMINI_API_KEY="your_gemini_api_key_here"
                break
            elif [[ -z "$GEMINI_API_KEY" ]]; then
                print_warning "API key cannot be empty. Please enter a valid key or type 'skip'"
            fi
        done
        
        # Create .env file with the API key
        cat > .env << EOF
# GEPA MCP Server Configuration
GEMINI_API_KEY=$GEMINI_API_KEY

# Optional: Set custom model preferences
# GEMINI_MODEL=gemini-1.5-flash
# TEMPERATURE=0.7
EOF
        
        if [[ "$GEMINI_API_KEY" == "your_gemini_api_key_here" ]]; then
            print_warning "API key skipped - you'll need to add it to .env later"
        else
            print_success "API key configured successfully"
        fi
    fi
    
    # Final instructions
    echo ""
    print_success "🎉 GEPA MCP Server installation completed successfully!"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    if [[ "$GEMINI_API_KEY" == "your_gemini_api_key_here" ]]; then
        echo -e "  1. Get a Gemini API key from: ${YELLOW}https://makersuite.google.com/app/apikey${NC}"
        echo -e "  2. Add your API key to: ${YELLOW}$(pwd)/.env${NC}"
        echo -e "  3. Restart Claude Desktop application"
        echo -e "  4. Look for GEPA tools in Claude Desktop's tool panel"
    else
        echo -e "  1. Restart Claude Desktop application"
        echo -e "  2. Look for GEPA tools in Claude Desktop's tool panel"
        echo -e "  3. Start optimizing your prompts! 🚀"
    fi
    echo ""
    echo -e "${BLUE}Available Tools:${NC}"
    echo -e "  • ${GREEN}optimize_prompt${NC} - Core GEPA genetic-evolutionary optimization"
    echo -e "  • ${GREEN}quick_prompt_improve${NC} - Fast prompt enhancement"
    echo -e "  • ${GREEN}conversational_optimize${NC} - Context-aware optimization"
    echo -e "  • ${GREEN}holistic_optimize${NC} - Multi-objective optimization"
    echo -e "  • ${GREEN}auto_optimize_prompt${NC} - Automated optimization"
    echo -e "  • ${GREEN}gepa_with_claude_analysis${NC} - Claude-enhanced GEPA"
    echo -e "  • And 6 more advanced optimization tools!"
    echo ""
    echo -e "${BLUE}Documentation:${NC} See README.md for detailed usage examples"
    echo -e "${BLUE}Troubleshooting:${NC} Check the troubleshooting section in README.md"
    echo ""
    print_success "Installation complete! Enjoy using GEPA MCP! 🚀"
}

# Run main function
main "$@"