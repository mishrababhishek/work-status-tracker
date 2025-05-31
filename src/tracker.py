from datetime import datetime
from git import Repo, NULL_TREE
from utils.settings import get_config
from utils.logger import log

def get_changes() -> str:
    log("[get_changes] Fetching changes from the repositories ...")
    
    repos = get_config("repos")
    if not repos:
        log("[get_changes] No repositories found in configuration.")
        return ""

    today = datetime.now().date()
    result_lines = []

    for repo_cfg in repos:
        repo_path = repo_cfg['path']
        branch = repo_cfg['branch']
        log(f"[get_changes] Processing repository at: {repo_path} | Branch: {branch}")

        try:
            repo = Repo(repo_path)
        except Exception as e:
            log(f"[get_changes] Failed to open repository at '{repo_path}': {e}")
            continue

        try:
            log(f"[get_changes] Checking out branch '{branch}'")
            repo.git.checkout(branch)
        except Exception as e:
            log(f"[get_changes] Error checking out branch '{branch}' in repo '{repo_path}': {e}")
            continue

        try:
            commits = [c for c in repo.iter_commits(branch) if c.committed_datetime.date() == today]
            log(f"[get_changes] Found {len(commits)} commit(s) for today in '{repo_path}' on branch '{branch}'")
        except Exception as e:
            log(f"[get_changes] Failed to fetch commits for branch '{branch}' in repo '{repo_path}': {e}")
            continue

        if not commits:
            continue

        result_lines.append(f"=== Repository: {repo_path} (branch: {branch}) ===")

        for commit in commits:
            log(f"[get_changes] Processing commit: {commit.hexsha}")
            result_lines.append(f"--- Commit: {commit.hexsha} ---")
            result_lines.append(f"Message: {commit.message.strip()}\n")

            try:
                diffs = commit.diff(commit.parents[0] if commit.parents else NULL_TREE, create_patch=True)
                log(f"[get_changes] Found {len(diffs)} file diff(s) in commit {commit.hexsha}")
            except Exception as e:
                log(f"[get_changes] Failed to generate diff for commit {commit.hexsha}: {e}")
                continue

            for diff in diffs:
                try:
                    change_type = diff.change_type
                    file_path = diff.a_path if diff.a_path else diff.b_path
                    result_lines.append(f"File: {file_path} | Change: {change_type}")
                    log(f"[get_changes] Processing diff for file: {file_path} | Change: {change_type}")

                    diff_text = diff.diff.decode('utf-8', errors='ignore')
                    diff_lines = diff_text.splitlines()
                    max_lines = 50

                    if len(diff_lines) > max_lines:
                        truncated = diff_lines[:max_lines]
                        truncated.append(f"... [Diff truncated: total {len(diff_lines)} lines]")
                        diff_text = "\n".join(truncated)
                        log(f"[get_changes] Diff for '{file_path}' truncated to {max_lines} lines")

                    result_lines.append(diff_text)
                    result_lines.append("")
                except Exception as e:
                    log(f"[get_changes] Error processing diff for file in commit {commit.hexsha}: {e}")
                    continue

        result_lines.append(f"{'=' * 40}\n")

    log("[get_changes] Finished processing all repositories.")
    return "\n".join(result_lines)
