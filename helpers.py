import subprocess

def get_commit_desc(commit_hash: str, CWD: str) -> str:
    try:
        command = f"hg log -r {commit_hash} --template '{{desc}}'"
        return subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )
    except Exception as e:
        raise Exception(str(e))

def get_commit_diff(commit_hash: str, CWD: str) -> str:
    try:
        command = f"hg diff -r {commit_hash}"
        return subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )
    except Exception as e:
        raise Exception(str(e))

def get_commit_stats(commit_hash: str, CWD: str) -> str:
    try:
        command = f"hg log -r {commit_hash} --stat"
        return subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=CWD
        )
    except Exception as e:
        raise Exception(str(e))
