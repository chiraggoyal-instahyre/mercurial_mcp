from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
import subprocess
import os
import helpers

mcp = FastMCP("Mercurial MCP", mask_error_details=True)

HG_REPO_ROOT = os.environ.get("HG_REPO_ROOT")

if not HG_REPO_ROOT:
    raise ValueError("HG_REPO_ROOT environment variable is not set")

if not os.path.exists(HG_REPO_ROOT) or not os.path.isdir(HG_REPO_ROOT):
    raise ValueError("HG_REPO_ROOT does not exist or is not a directory")

# get parent directory of HG_REPO_ROOT
CWD = os.path.dirname(HG_REPO_ROOT)

@mcp.tool()
def get_file_at_commit(commit_hash: str, file_path: str, head: int = None, tail: int = None) -> str:
    """
    Get the content of a file at a specific commit.

    Args:
        commit_hash: The hash of the commit.
        file_path: The path of the file.
        head: The number of lines to show from the end of the file.
        tail: The number of lines to show from the start of the file.

    Returns:
        The content of the file at the given commit.
    """
    try:
        relpath = os.path.relpath(file_path, CWD)
        command = f'hg cat {commit_hash} {relpath}'

        if head is not None:
            command += f" | head -n {head}"

        if tail is not None:
            command += f" | tail -n {tail}"

        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )

        if result.returncode != 0:
            raise ToolError(result.stderr.strip())

        return result.stdout.strip()
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool()
def blame_file(file_path: str, head: int = None, tail: int = None) -> str:
    """
    Blames/annotates the given file.

    Args:
        file_path: The path of the file.
        head: The number of lines to show from the end of the file.
        tail: The number of lines to show from the start of the file.

    Returns:
        The reponse is a string where each line is of the form:
        <commit_hash>, <parent_commit_hash>, <author>, <date|age>, <line_content>
    """
    try:
        relpath = os.path.relpath(file_path, CWD)
        command = "hg annotate --template '{lines % \"{pad(node|short,12,left=true)}, {pad(p1node|short,12,left=true)}, {pad(fill(author|emailuser|lower,11)|firstline,11,left=true)}, {pad(date|age|short,13,left=true)}, {line}\"}'"

        command += f" {relpath}"

        if head is not None:
            command += f" | head -n {head}"

        if tail is not None:
            command += f" | tail -n {tail}"

        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )

        if result.returncode != 0:
            raise ToolError(result.stderr.strip())

        return result.stdout.strip()
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool()
def log_commits(file_path: str = None, head: int = None, tail: int = None) -> str:
    """
    Returns the log of commits. If file_path is provided, returns the log of commits for that file.

    Args:
        file_path: The path of the file.
        head: The number of commits to show from the end of the log.
        tail: The number of commits to show from the start of the log.

    Returns:
        The log of commits.
    """
    try:
        command = "hg log"

        if file_path is not None:
            relpath = os.path.relpath(file_path, CWD)
            command += f" -f {relpath}"

        if head is not None:
            command += f" | head -n {head}"

        if tail is not None:
            command += f" | tail -n {tail}"

        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )

        if result.returncode != 0:
            raise ToolError(result.stderr.strip())

        return result.stdout.strip()
    except Exception as e:
        raise ToolError(str(e))

@mcp.tool()
def get_commit_summary(commit_hash: str) -> str:
    """
    Gets the summary of a commit.

    Args:
        commit_hash: The hash of the commit.

    Returns:
        The summary of the commit. Summary includes the description of the
        changes, stats and diff separated by respective heading.
    """
    try:
        desc = helpers.get_commit_desc(commit_hash, CWD)
        stats = helpers.get_commit_stats(commit_hash, CWD)
        diff = helpers.get_commit_diff(commit_hash, CWD)

        if desc.returncode != 0 or stats.returncode != 0 or diff.returncode != 0:
            raise ToolError(desc.stderr.strip() or stats.stderr.strip() or diff.stderr.strip())

        return f"""
        Description:
        {desc.stdout.strip()}

        Stats:
        {stats.stdout.strip()}

        Diff:
        {diff.stdout.strip()}
        """
    except Exception as e:
        raise ToolError(str(e))


@mcp.tool()
def search_across_files(pattern: str) -> str:
    """
    Searches for a pattern across all files in the repository. However,
    could be slow for large repositories, so, use when necessary.

    Args:
        pattern: The regex to search for.

    Returns:
        The list of files that contain the pattern along with the commit id.
    """
    try:
        command = f"hg grep --all '{pattern}'"
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )

        if result.returncode != 0:
            raise ToolError(result.stderr.strip())

        return result.stdout.strip()
    except Exception as e:
        raise ToolError(str(e))


if __name__ == "__main__":
    mcp.run()