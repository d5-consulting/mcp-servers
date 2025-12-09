import subprocess

from . import mcp


@mcp.tool()
def shell(command: str) -> str:
    """
    Execute a shell command and return the output.

    Args:
        command: Shell command to execute

    Returns:
        Command output (stdout, and stderr if present)
    """
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
