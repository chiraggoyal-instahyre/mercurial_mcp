import subprocess

clean_diff_command = """
  perl -0777 -pe '
    # Remove everything from "Test Plan:" till commit end
    s/Test Plan:.*?---END OF COMMIT---/---END OF COMMIT---/isg;

    # Split into lines, filter out specific unwanted lines, then reassemble
    @lines = grep {
      !/Summary:/ &&         # Remove lines containing "Summary:"
      !/Fixes T/ &&         # Remove lines containing "Fixes T"
      !/Part of T/ &&         # Remove lines containing "Part of T"
      !/\*\*Land on/ &&     # Remove lines containing "**Land on"
      !/Caused by:/ &&        # Remove lines containing "Caused by:"
      !/Reviewers:/ &&        # Remove lines containing "Reviewers:"
      !/Reviewed By:/ &&        # Remove lines containing "Reviewed By:"
      !/Maniphest Tasks:/ &&        # Remove lines containing "Maniphest Tasks:"
      !/Differential Revision:/ &&        # Remove lines containing "Differential Revision:"
      !/Reason for not mentioning/     # Remove lines containing "Reason for not mentioning"
    } split /\n/;

    $_ = join("\n", @lines) . "\n";

    # Remove any files, revisions, or tasks
    s/{F\d+}//g;
    s/D\d+//g;
    s/T\d+//g;

    # Remove formatting
    s/\*\*//g;  # Remove bold formatting
    s/\/\///g;  # Remove italic formatting

    # Remove attached URLs (keeping the name)
    s/\[\[\s*[^|\]]+\|\s*([^\]]+)\s*\]\]/$1/g;

    # Normailize line breaks
    s/\n{2,}/\n\n/g;  # Replace three or more newlines with two newlines
  '
"""

def get_commit_desc(commit_hash: str, CWD: str) -> str:
    try:
        command = f"hg log -r {commit_hash} --template '{{desc}}' | {clean_diff_command}"
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
