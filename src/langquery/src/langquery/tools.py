import subprocess

import duckdb

from . import mcp

# ======================================================
# core
# ======================================================


@mcp.tool()
def shell(command: str) -> str:
    """execute a shell command and return the output"""
    res = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )
    output = res.stdout

    if err := res.stderr:
        output = f"**stdout**: {output}\n\n**stderr**: {err}"

    return output


@mcp.tool()
def query(sql: str) -> str:
    """execute a duckdb sql query and return the result as text."""
    db = duckdb.connect(database=":memory:")
    result = db.execute(sql).fetchdf()
    return result.to_markdown(index=False)


# ======================================================
# basic math operations
# ======================================================


@mcp.tool()
def add(a: int | float, b: int | float) -> int | float:
    """add numbers"""
    return a + b


@mcp.tool()
def sub(a: int | float, b: int | float) -> int | float:
    """sub numbers"""
    return a - b


@mcp.tool()
def mul(a: int | float, b: int | float) -> int | float:
    """multiply numbers"""
    return a * b


@mcp.tool()
def div(a: int | float, b: int | float) -> float:
    """divide numbers"""
    return a / b
