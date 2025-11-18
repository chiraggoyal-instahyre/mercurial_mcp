# Mercurial MCP Server (FastMCP)

Minimal MCP server exposing Mercurial and Arcanist utilities to MCP-compatible clients (e.g., Windsurf) over stdio.

Tools provided (see `server.py`):
- `get_file_at_commit`
- `blame_file`
- `log_commits`
- `get_commit_summary`
- `search_across_files`
- `get_revision_summary_by_id`
- `get_revision_changes_by_id`
- `get_task_summary_by_id`

## How to set up the project

- **Prerequisites**
  - Python 3.9+
  - Mercurial (`hg`) available on PATH
  - Optional (for revision/task tools): Arcanist (`arc`) configured with access

- **Install dependencies**
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # Linux/macOS
  # On Windows: .venv\\Scripts\\activate

  pip install --upgrade pip
  pip install -r requirements.txt
  ```

- **Environment variables**
  - `HG_REPO_ROOT` (required): absolute path to the repo's `.hg` directory (e.g., `/path/to/repo/.hg`)
  - `TOKEN_LIMIT` (optional): character budget for paging large outputs (default: 4096)

- **Local run (manual test)**
  ```bash
  export HG_REPO_ROOT=/abs/path/to/your/repo/.hg
  export TOKEN_LIMIT=4096  # optional
  python server.py
  ```
  The server is intended to be launched by an MCP client over stdio; the above only verifies it starts without errors.

## How to add Mercurial MCP to Windsurf (stdio)

You can add this server to Windsurf as a custom MCP server using stdio.

  Example entry for your Windsurf MCP config (adapt to your file format/location):
  ```json
  {
    "mercurial": {
      "command": "/home/chirag/repo/mercurial_mcp/run.sh",
      "args": [],
      "env": {
        "HG_REPO_ROOT": "/home/chirag/repo/devel/.hg",
        "TOKEN_LIMIT": "10000"
      },
      "disabled": false,
      "disabledTools": [
        "search_across_files"
      ]
    }
  }
  ```

### Update run.sh

Create or update `run.sh` and launch the server:

```bash
#!/bin/bash
cd /home/chirag/repo/mercurial_mcp/
source .venv/bin/activate
python3 server.py
```

Make it executable:
```bash
chmod +x /home/chirag/repo/mercurial_mcp/run.sh
```

- **Verification**
  - In Windsurf, open the MCP panel and confirm the server is listed as "Mercurial MCP".
  - Tools from `server.py` should appear and be callable.

## Notes
- Commands that depend on Arcanist (e.g., `get_revision_*`, `get_task_*`) require `arc` and appropriate auth.
- Large outputs are paginated using `TOKEN_LIMIT`; request subsequent pages with the `page` parameter where applicable.