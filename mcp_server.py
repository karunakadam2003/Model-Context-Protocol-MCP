from mcp.server.fastmcp import FastMCP
import os
import requests
from typing import List, Dict
import json

# Initialize MCP server
mcp = FastMCP("MultiToolMCPServer")

# Tool 1: File Operations - Read a file
@mcp.tool()
def read_file(filepath: str) -> str:
    """Read content from a specified file path."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Tool 2: File Operations - Write to a file
@mcp.tool()
def write_file(filepath: str, content: str) -> str:
    """Write content to a specified file path."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Tool 3: Calculator - Basic arithmetic
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic arithmetic operations."""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    print("In Calculate tool")
    try:
        result = operations.get(operation.lower(), lambda x, y: "Invalid operation")(a, b)
        return result
    except Exception as e:
        return f"Calculation error: {str(e)}"

# Tool 4: Web Scraping - Fetch webpage title
@mcp.tool()
def get_webpage_title(url: str) -> str:
    """Fetch the title of a webpage from a given URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return title.strip()
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"

# Resource: Provide a list of available files in a directory
@mcp.resource(uri="/list_directory/{path}")
def list_directory(path: str) -> List[Dict[str, str]]:
    """List files in a specified directory."""
    try:
        files = []
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            files.append({
                "name": entry,
                "type": "directory" if os.path.isdir(full_path) else "file",
                "path": full_path
            })
        return files
    except Exception as e:
        return [{"error": f"Error listing directory: {str(e)}"}]

# Prompt: Predefined template for summarizing files
@mcp.prompt()
def summarize_file_prompt() -> str:
    """Provide a prompt template for summarizing file content."""
    return """
    Please summarize the content of the file provided below in 100 words or less.
    File content: {{ content }}
    """

# Start the MCP server
if __name__ == "__main__":
    print("Starting MCP Server: MultiToolMCPServer")
    mcp.run()