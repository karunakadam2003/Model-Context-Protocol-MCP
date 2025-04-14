import subprocess
import time
import os
import signal
from mcp.client import MCPClient

class MCPHost:
    def __init__(self, server_script: str):
        self.server_script = server_script
        self.process = None

    def start_server(self):
        """Start the MCP server as a subprocess."""
        if self.process is None:
            print(f"Starting MCP server from {self.server_script}...")
            # Run server in a subprocess
            self.process = subprocess.Popen(
                ["python", self.server_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Wait briefly to ensure server starts
            time.sleep(2)
            if self.process.poll() is not None:
                print("Server failed to start:", self.process.stderr.read())
                self.process = None
                return False
            print("MCP server started successfully.")
            return True
        return False

    def stop_server(self):
        """Stop the MCP server."""
        if self.process is not None:
            print("Stopping MCP server...")
            # Send SIGTERM to gracefully stop the server
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server did not stop gracefully, forcing termination...")
                self.process.kill()
            self.process = None
            print("MCP server stopped.")
        else:
            print("No server is running.")

    def test_connection(self):
        """Test if the server is responsive by connecting a client."""
        client = MCPClient("MultiToolMCPServer", transport="stdio")
        try:
            capabilities = client.discover()
            print("Server is responsive. Capabilities:", capabilities)
            return True
        except Exception as e:
            print(f"Failed to connect to server: {str(e)}")
            return False
        finally:
            client.close()

if __name__ == "__main__":
    # Initialize host with the server script
    host = MCPHost("mcp_server.py")

    # Start the server
    if host.start_server():
        # Test connection
        if host.test_connection():
            print("Host: Server is running and responsive.")
        else:
            print("Host: Server started but is not responsive.")
        
        # Keep server running for a bit to simulate usage
        print("Host: Letting server run for 10 seconds...")
        time.sleep(10)
        
        # Stop the server
        host.stop_server()
    else:
        print("Host: Failed to start server.")
        
