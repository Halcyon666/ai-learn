from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Simple-Math-Server")


@mcp.tool()
def add_numbers(a: int, b: int) -> dict:
    """Add two numbers together and return a structured object."""
    total = a + b

    # Return a dictionary that matches your desired "properties" structure
    return {
        "result": total
    }


if __name__ == "__main__":
    mcp.run()