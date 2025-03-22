# LinkedIn MCP Server

A Model Context Protocol (MCP) server implementation for interacting with LinkedIn data using Claude AI. This server provides tools to fetch LinkedIn profiles, search jobs, and generate PDF CVs using the LinkedIn API.

## Features

- Fetch detailed LinkedIn profile data
- Search for jobs with advanced filters
- Generate PDF CVs from LinkedIn profiles
- Integration with Claude AI Desktop

## Prerequisites

- Python 3.8+
- Claude AI Desktop
- RapidAPI Key for LinkedIn APIs
- MCP SDK

## Installation

1. First, install `uv` package manager by following the instructions at [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/). Here are the quick install commands:

   **For macOS and Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   **For Windows:**
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LinkedInMCP.git
   cd LinkedInMCP
   ```

3. Install dependencies using uv:
   ```bash
   uv sync
   ```
   This will automatically install all required dependencies from the project configuration.

4. Create a `.env` file in the project root:
   ```plaintext
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```

## Claude AI Desktop Setup

To integrate with Claude AI Desktop, create or modify the configuration file at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:
```json
{
  "mcpServers": {
    "ProjectMCP": {
      "command": "/Users/username/.local/bin/uv",  // Path to your uv installation
      "args": [
        "--directory",
        "/path/to/ProjectMCP",
        "run",
        "linkedIn.py"
      ]
    }
  }
}
```

Note: Replace `/Users/username/.local/bin/uv` with your actual uv installation path. You can find this by running:
```bash
which uv  # On macOS/Linux
where uv  # On Windows
```


## Available Tools

1. `get_profile`: Fetch LinkedIn profile data
   - Input: LinkedIn profile URL
   - Output: JSON formatted profile data

2. `get_jobs`: Search for jobs on LinkedIn
   - Inputs: 
     - keywords (required)
     - geo_code (optional)
     - date_posted (optional)
     - company_id (optional)

3. `get_pdf_cv`: Generate PDF CV from LinkedIn profile
   - Input: LinkedIn profile URL
   - Output: PDF file or success message

## Running the Server

Currently, the server runs using STDIO transport:
```bash
python linkedIn.py
```

### Transport Modes

This project currently uses STDIO transport, which is ideal for development and testing. Future implementations will include SSE (Server-Sent Events) transport.

#### STDIO vs SSE Transport: 

- **STDIO Transport**:
  - Simple command-line based communication
  - Ideal for development and testing
  - Direct integration with Claude AI Desktop
  - Limited to local machine communication

- **SSE Transport** (Future Implementation):
  - Web-based communication protocol
  - Enables remote server deployment
  - Better for production environments
  - Supports multiple concurrent clients
  - Can be integrated with web frameworks like FastAPI or Starlette

## Credits 

Required Documentation:
- [Model Context Protocol (MCP) Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Documentation](https://modelcontextprotocol.io/docs/concepts/tools)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
