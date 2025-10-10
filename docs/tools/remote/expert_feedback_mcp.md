# Human Expert Feedback System MCP

This system allows ToolUniverse to consult human experts for complex decisions through an MCP (Model Context Protocol) server.

<img width="1504" height="729" alt="image" src="https://github.com/user-attachments/assets/f24229ca-fc6f-40ca-a0b4-073cf7df370f" />

## Quick Start

### Environment Setup

Before starting the system, you need to note the MCP server URL that will be displayed when you run the server.

**Step 1: Start the MCP Server first to see the URL**
```bash
python human_expert_mcp_server.py
```

When the server starts, it will display:
```
🚀 MCP Server running on http://0.0.0.0:7001
```

**Step 2: Set the environment variable**
Based on the displayed URL, set the environment variable (use `localhost:7001` for the environment variable):
```bash
export EXPERT_FEEDBACK_MCP_SERVER_URL="localhost:7001"
```

Or create a `.env` file (copy from `.env.template`) and set:
```bash
EXPERT_FEEDBACK_MCP_SERVER_URL=localhost:7001
```

**Important**:
- The server runs on `http://0.0.0.0:7001` but the environment variable should be set to `localhost:7001` (without `http://` prefix)
- The server URL will be shown when you run `human_expert_mcp_server.py`

### System Components

The system consists of three separate components that should be started independently:

### 1. Start the MCP Server
```bash
python human_expert_mcp_server.py
```
This starts the MCP server on port 7001 that ToolUniverse can connect to.

### 2. Start the Web Interface (Recommended)
```bash
python start_web_interface.py
```
This provides a web-based interface for experts to view and respond to requests.

### 3. Start the Terminal Interface (Alternative)
```bash
python human_expert_mcp_server.py --interface-only
```
This provides a command-line interface for experts to view and respond to requests.

## Usage Workflow

1. **Start the MCP server first**: `python human_expert_mcp_server.py`
2. **Note the server URL displayed**: The server will show `🚀 MCP Server running on http://0.0.0.0:7001`
3. **Set Environment Variable**: `export EXPERT_FEEDBACK_MCP_SERVER_URL=localhost:7001`
4. **Start either the web interface OR terminal interface** (for experts to monitor requests)
5. **Use ToolUniverse** with the expert consultation tools to submit questions
6. **Experts respond** through their chosen interface
7. **ToolUniverse retrieves responses** using the response tools

### Recommended Startup Workflow

**Terminal 1 - MCP Server (Start this first):**
```bash
python human_expert_mcp_server.py
# Note the URL displayed: 🚀 MCP Server running on http://0.0.0.0:7001
```

**Terminal 2 - Set environment variable and start Expert Interface:**

**Set the environment variable:**
```bash
export EXPERT_FEEDBACK_MCP_SERVER_URL="localhost:7001"
```

**Then choose one interface:**

**Web Interface (Recommended):**
```bash
python start_web_interface.py
```

**OR Terminal Interface:**
```bash
python human_expert_mcp_server.py --interface-only
```

**Terminal 3 - ToolUniverse:**
```bash
# Make sure EXPERT_FEEDBACK_MCP_SERVER_URL is set in this terminal too
export EXPERT_FEEDBACK_MCP_SERVER_URL="localhost:7001"
# Then use ToolUniverse with expert consultation tools
```

### Alternative Direct Commands

Instead of using the convenience scripts, you can run directly:

```bash
# MCP server only (default)
python human_expert_mcp_server.py

# Web interface only
python human_expert_mcp_server.py --web-only

# Terminal interface only
python human_expert_mcp_server.py --interface-only
```

## Available MCP Tools

- `consult_human_expert`: Submit questions to human experts
- `get_expert_response`: Check for expert responses
- `list_pending_expert_requests`: View pending requests (for experts)
- `submit_expert_response`: Submit expert responses (for experts)
- `get_expert_status`: Get system status

## ToolUniverse Integration

The tools are configured in `src/tooluniverse/data/expert_feedback_tools.json`. The configuration uses the `EXPERT_FEEDBACK_MCP_SERVER_URL` environment variable to determine the server URL.

**Important Configuration Steps**:
1. **Start the MCP server first** to see the URL it displays
2. **Set the environment variable** based on the server output:
```bash
export EXPERT_FEEDBACK_MCP_SERVER_URL="localhost:7001"
```

The configuration file expects this format: `localhost:7001` (without `http://` prefix), even though the server displays `http://0.0.0.0:7001`.

To use these tools through ToolUniverse:

1. **Start the MCP server** and note the displayed URL
2. **Set the environment variable** (required for the MCP connection)
3. **Make sure the MCP server is running** on port 7001
4. **Load tools in ToolUniverse** and they will be available with the `expert_` prefix:
   - `expert_consult_human_expert`
   - `expert_get_expert_response`
   - `expert_list_pending_expert_requests`
   - `expert_submit_expert_response`
   - `expert_get_expert_status`

Example usage:
```python
import os
from tooluniverse import ToolUniverse

# Make sure EXPERT_FEEDBACK_MCP_SERVER_URL is set before importing
os.environ['EXPERT_FEEDBACK_MCP_SERVER_URL'] = 'localhost:7001'

tooluni = ToolUniverse()
tooluni.load_tools()

result = tooluni.run({
    "name": "expert_consult_human_expert",
    "arguments": {
        "question": "What is the recommended dosage of aspirin for elderly patients?",
        "specialty": "cardiology",
        "priority": "normal"
    }
})
```

## Requirements

- Python 3.8+
- fastmcp
- Flask (for web interface)
- requests

## Installation

```bash
pip install fastmcp flask requests
```

## Configuration

The system uses default ports:
- MCP Server: 7001
- Web Interface: 8080

These can be modified in the respective script files if needed.

**Environment Variables:**
- `EXPERT_FEEDBACK_MCP_SERVER_URL`: Must be set to `localhost:7001` for the system to work properly

## File Overview

- `human_expert_mcp_server.py` - Main MCP server (can run all modes)
- `start_web_interface.py` - Convenience script for web interface
- `simple_test.py` - Simple test script
- `README.md` - This documentation
- `requirements.txt` - Dependencies
- `.env.template` - Environment variable template
- `src/tooluniverse/data/expert_feedback_tools.json` - ToolUniverse configuration

## System Architecture

The system has a clean, modular design with three independent components:

1. **MCP Server** (`human_expert_mcp_server.py`) - Core server that handles expert consultation requests
2. **Web Interface** (`start_web_interface.py`) - User-friendly web interface for experts
3. **Terminal Interface** (built into MCP server with `--interface-only` flag) - Command-line interface for experts

### Key Improvements

✅ Removed redundant startup scripts
✅ Simplified startup process - each component runs independently
✅ Clear separation of concerns - no complex "full system" mode
✅ Updated documentation to reflect new workflow
✅ Added ToolUniverse integration configuration
✅ Maintained all functionality while reducing complexity

Each component now has a single, clear responsibility and can be started independently.

## Testing

### Simple Test Script

A simple test script is provided to verify the system works:

```bash
# Step 1: Start the MCP server first (in another terminal)
python human_expert_mcp_server.py
# Note the displayed URL: 🚀 MCP Server running on http://0.0.0.0:7001

# Step 2: Set the environment variable
export EXPERT_FEEDBACK_MCP_SERVER_URL="localhost:7001"

# Step 3: Run the test
python simple_test.py
```

This test will submit a sample medical question and show the result.

### Manual Testing Workflow

1. **Start the MCP server** and note the displayed URL (`http://0.0.0.0:7001`)
2. **Set the environment variable** to `localhost:7001`
3. **Start the web interface** as described above
4. **Submit a test question** using ToolUniverse or the test script
5. **Check the web interface** at `http://localhost:8080` to see the pending request
6. **Submit a response** through the web interface
7. **Retrieve the response** using ToolUniverse

Make sure both the MCP server and web interface are running before testing.
