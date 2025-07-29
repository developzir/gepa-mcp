# GEPA MCP Server - Quick Install Guide

> Get up and running with GEPA optimization in under 5 minutes! 

## 🚀 One-Command Installation

```bash
./install.sh
```

That's it! The script will handle everything automatically.

## 📋 What the installer does:

✅ **Checks Prerequisites**
- Verifies Python 3.10+ is installed
- Installs `uv` package manager if needed

✅ **Installs Dependencies** 
- Automatically installs all required packages
- Sets up the virtual environment

✅ **Configures Claude Desktop**
- Detects your OS and finds the correct config file
- Backs up existing configuration 
- Adds GEPA MCP server configuration

✅ **Sets Up API Key**
- Prompts for your Gemini API key
- Creates .env file with proper configuration
- Validates the key format

✅ **Tests Installation**
- Verifies the server starts correctly
- Shows available tools and features

## 🔑 Getting Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key when prompted by the installer

## 🔧 Manual Configuration (if needed)

### Claude Desktop Config Locations:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude-desktop/claude_desktop_config.json`  
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

### Config Format:
```json
{
  "mcpServers": {
    "gepa-mcp": {
      "command": "uv",
      "args": ["run", "python", "run_server.py"],
      "cwd": "/full/path/to/GEPA-mcp"
    }
  }
}
```

## ⚡ Quick Test

After installation:

1. **Restart Claude Desktop**
2. **Look for GEPA tools** in the available tools panel
3. **Try a quick optimization**:
   ```
   Use the quick_prompt_improve tool to enhance: "Write me a summary"
   ```

## 🆘 Need Help?

- **Installation Issues**: See troubleshooting section in README.md
- **API Key Problems**: Verify it's correctly added to `.env` file
- **Tools Not Showing**: Restart Claude Desktop and check config file path

---

**🎉 Ready to optimize?** Your GEPA MCP server is installed and ready to supercharge your prompts!