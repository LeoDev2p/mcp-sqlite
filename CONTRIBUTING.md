# Contributing to MCP SQLite

Thank you for your interest in contributing! This document guides you through the steps to contribute to the project.

## Before You Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/mcp_sqlite.git
   cd mcp_sqlite
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Local Setup

```bash
# Install dependencies
uv sync

# Activate the virtual environment
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Verify everything works
fastmcp dev server.py
```

## Types of Contributions

### 1. New Tools

Add useful functionality to the MCP server:

```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Clear description of what this tool does."""
    query = "SELECT ..."
    result = await sqlite_connection(query, is_select=True)
    log.info(f"Tool executed: {param}")
    return result
```

**Requirements:**
- Use `async/await`
- Include descriptive docstring
- Use `prepared statements` (placeholders `?`)
- Log with `log.info()` or `log.error()`

### 2. Logging Improvements

Optimize or expand the logging system in `src/setting/logger.py`

### 3. Bugfixes

Fix bugs in:
- Error handling
- Input validation
- Documentation

### 4. Documentation

- Improve the README
- Add examples
- Fix typos
- Translate sections

## Before Making a PR

1. **Test your code:**
   ```bash
   fastmcp dev server.py
   ```

2. **Verify your code:**
   - Follow the existing style
   - Use clear variable and function names
   - Include docstrings in English or Spanish
   - Group imports: stdlib, third-party, local

3. **Update the documentation:**
   - If it's a new tool, add it to the README
   - Include usage examples
   - Document parameters and return types

## PR Process

1. **Commit with clear message:**
   ```bash
   git commit -m "feat: add new query optimization tool"
   git commit -m "fix: handle connection timeout error"
   git commit -m "docs: improve logging section in README"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub with:
   - Descriptive title
   - Description of what changes it makes
   - Problem it solves (if applicable)
   - Testing performed

## Project Structure

```
mcp_sqlite/
├── src/
│   ├── setting/          # Configuration and logging
│   │   ├── config.py     # Environment variables
│   │   └── logger.py     # Logging system
│   └── sqlite_mcp/       # MCP server
│       └── server.py     # Tools and connection
├── logs/                 # Server logs
├── README.md
├── CONTRIBUTING.md       # This file
└── pyproject.toml
```

## Advanced: Extending the Server

### Adding New Async Tools

To add new functionality to the MCP server:

1. Open `src/sqlite_mcp/server.py`
2. Add a new `@mcp.tool()` decorated async function:

```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Clear description of what this tool does."""
    query = "SELECT ..."
    result = await sqlite_connection(query, is_select=True)
    log.info(f"New tool executed: {param}")
    return result
```

3. Restart Claude Desktop or Antigravity
4. The new tool will be available automatically

### Logging in Custom Tools

Use the logger to track tool execution:

```python
log.info(f"Processing query: {query}")
try:
    result = await sqlite_connection(query)
except Exception as e:
    log.error(f"Tool error: {str(e)}")
    raise
```

### Testing Your Tools

Use `fastmcp dev` to test interactively:

```bash
fastmcp dev server.py

# In the interactive shell:
>>> await my_new_tool('test-param')
```

## Questions or Doubts

- Open an **Issue** to report bugs
- Open a **Discussion** for feature proposals
- Check existing issues before reporting


---

**Thank you for your contribution!**
