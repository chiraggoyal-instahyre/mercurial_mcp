from fastmcp import FastMCP
import subprocess
import os

CWD = "/home/chirag/repo/devel/auction"
mcp = FastMCP("Mercurial MCP")

@mcp.tool()
def get_file_at_commit(commit_hash: str, file_path: str) -> str:
    """
    Get the content of a file at a specific commit.
    """
    try:       
        relpath = os.path.relpath(file_path, CWD)
        command = f'hg cat {commit_hash} {relpath}'
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )

        if result.returncode != 0:
            return f"cwd: {CWD}\ncommand: {command}\nerror: {result.stderr}"

        return result.stdout
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run()