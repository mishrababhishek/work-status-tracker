from datetime import datetime
from git import Repo, NULL_TREE
from utils.settings import get_config
from utils.logger import log

def get_changes() -> str:
    log("Fetching changes from the repositories ...")
    repos = get_config("repos")
    today = datetime.now().date()
    result_lines = []

    for repo_cfg in repos:
        repo_path = repo_cfg['path']
        branch = repo_cfg['branch']
        repo = Repo(repo_path)

        try:
            log(f"Checking out branch '{branch}' in repo '{repo_path}'")
            repo.git.checkout(branch)
        except Exception as e:
            log(f"Error checking out branch '{branch}' in repo '{repo_path}': {e}")
            continue

        commits = [c for c in repo.iter_commits(branch) if c.committed_datetime.date() == today]
        log(f"Found {len(commits)} commits for today in repo '{repo_path}' branch '{branch}'")

        if not commits:
            continue

        result_lines.append(f"=== Repository: {repo_path} (branch: {branch}) ===")
        for commit in commits:
            result_lines.append(f"--- Commit: {commit.hexsha} ---")
            result_lines.append(f"Message: {commit.message.strip()}\n")
            diffs = commit.diff(commit.parents[0] if commit.parents else NULL_TREE, create_patch=True)

            for diff in diffs:
                change_type = diff.change_type
                file_path = diff.a_path if diff.a_path else diff.b_path
                result_lines.append(f"File: {file_path} | Change: {change_type}")

                diff_text = diff.diff.decode('utf-8', errors='ignore')

                max_lines = 50
                diff_lines = diff_text.splitlines()
                if len(diff_lines) > max_lines:
                    truncated = diff_lines[:max_lines]
                    truncated.append(f"... [Diff truncated: total {len(diff_lines)} lines]")
                    diff_text = "\n".join(truncated)

                result_lines.append(diff_text)
                result_lines.append("")

        result_lines.append(f"{'='*40}\n")

    return "\n".join(result_lines)
