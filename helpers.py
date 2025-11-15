import asyncio

async def run_command_async(command: str, cwd: str) -> str:
    """
    Common method to run commands asynchronously.
    
    Args:
        command: The command to execute
        cwd: Working directory for the command
        
    Returns:
        Decoded stdout from the command
        
    Raises:
        Exception: If command fails with non-zero return code
    """
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(stderr.decode().strip())
        
        return stdout.decode().strip()
    except Exception as e:
        raise Exception(str(e))

async def get_commit_desc(commit_hash: str, CWD: str):
    command = f"hg log -r {commit_hash} --template '{{desc}}'"
    return await run_command_async(command, CWD)

async def get_commit_diff(commit_hash: str, CWD: str):
    command = f"hg diff -r {commit_hash}"
    return await run_command_async(command, CWD)
