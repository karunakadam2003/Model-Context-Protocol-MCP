# import asyncio
# import json
# import os
# from mcp.client.stdio import stdio_client, StdioServerParameters

# async def run_client():
#     test_file = "test.txt"

#     # Get the current directory
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     server_path = os.path.join(current_dir, "mcp_server.py")

#     # Proper async context manager with StdioServerParameters
#     async with stdio_client(StdioServerParameters(command="python", args=[server_path])) as (client, _):
#         try:
#             print("Discovering server capabilities...")
#             capabilities = await client.discover()
#             print("Available tools:", [tool["name"] for tool in capabilities.get("tools", [])])
#             print("Available resources:", [res["name"] for res in capabilities.get("resources", [])])
#             print("Available prompts:", [prompt["name"] for prompt in capabilities.get("prompts", [])])

#             # Demo 1: Calculate (5 + 3)
#             print("\nInvoking calculate tool...")
#             result = await client.invoke_tool("calculate", {"operation": "add", "a": 5, "b": 3})
#             print("Result of calculate(add, 5, 3):", result)

#             # Demo 2: Write and read a file
#             print("\nInvoking write_file tool...")
#             content = "Hello, this is a test file created via MCP!"
#             result = await client.invoke_tool("write_file", {"filepath": test_file, "content": content})
#             print("Result of write_file:", result)

#             print("\nInvoking read_file tool...")
#             result = await client.invoke_tool("read_file", {"filepath": test_file})
#             print("Content of test.txt:", result)

#             # Demo 3: Get webpage title
#             print("\nInvoking get_webpage_title tool...")
#             result = await client.invoke_tool("get_webpage_title", {"url": "https://example.com"})
#             print("Webpage title of https://example.com:", result)

#             # Demo 4: List current directory
#             print("\nInvoking list_directory resource...")
#             result = await client.invoke_resource("list_directory", {"path": "."})
#             print("Files in current directory:", json.dumps(result, indent=2))

#             # Demo 5: Use summarize_file_prompt
#             print("\nInvoking summarize_file_prompt...")
#             result = await client.invoke_prompt("summarize_file_prompt", {})
#             prompt_template = result
#             file_content = await client.invoke_tool("read_file", {"filepath": test_file})
#             filled_prompt = prompt_template.replace("{{ content }}", file_content)
#             print("Filled prompt for summarization:", filled_prompt)

#         except Exception as e:
#             print(f"Client error: {str(e)}")
#         finally:
#             if os.path.exists(test_file):
#                 os.remove(test_file)

# if __name__ == "__main__":
#     print("Starting MCP Client")
#     asyncio.run(run_client())



import asyncio
import json
import os
from awesome_mcp_clients.cursor import MCPClient  # Correct path based on repo structure

async def run_client():
    test_file = "test.txt"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "mcp_server.py")

    # Start the MCP client using the cursor-based approach
    async with MCPClient(server_path) as client:
        try:
            # Discover server capabilities
            capabilities = await client.discover()
            print("Available tools:", [tool["name"] for tool in capabilities.get("tools", [])])

            # Demo 1: Calculate (5 + 3)
            result = await client.invoke_tool("calculate", {"operation": "add", "a": 5, "b": 3})
            print("Result of calculate(add, 5, 3):", result)

            # Demo 2: Write and read a file
            content = "Hello, this is a test file created via MCP!"
            await client.invoke_tool("write_file", {"filepath": test_file, "content": content})
            result = await client.invoke_tool("read_file", {"filepath": test_file})
            print("Content of test.txt:", result)

            # Demo 3: Get webpage title
            result = await client.invoke_tool("get_webpage_title", {"url": "https://example.com"})
            print("Webpage title:", result)

            # Demo 4: List current directory
            result = await client.invoke_resource("list_directory", {"path": "."})
            print("Files in current directory:", json.dumps(result, indent=2))

            # Demo 5: Summarize file content
            prompt_template = await client.invoke_prompt("summarize_file_prompt", {})
            file_content = await client.invoke_tool("read_file", {"filepath": test_file})
            filled_prompt = prompt_template.replace("{{ content }}", file_content)
            print("Filled prompt for summarization:", filled_prompt)

        except Exception as e:
            print(f"Client error: {str(e)}")
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == "__main__":
    print("Starting MCP Client")
    asyncio.run(run_client())
