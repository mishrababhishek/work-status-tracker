import datetime
from typing import Optional, Tuple
from git import Repo, NULL_TREE
from difflib import unified_diff

def get_git_changes_today(repo_path: str, branch: str = "main") -> Tuple[bool, Optional[str]]:
    repo = Repo(repo_path)
    today = datetime.datetime.now().date()
    output = []

    commits_today = [
        c for c in repo.iter_commits(branch, max_count=100)
        if datetime.datetime.fromtimestamp(c.committed_date).date() == today
    ]

    if not commits_today:
        return False, None

    for commit in commits_today:
        output.append(f"\n--- Commit: {commit.hexsha[:7]} | {commit.author.name} | {commit.committed_datetime} ---")
        
        if commit.parents:
            diff_index = commit.diff(commit.parents[0])
        else:
            diff_index = commit.diff(NULL_TREE)

        for diff in diff_index:
            change_type = {'M': 'Modified', 'A': 'Added', 'D': 'Deleted'}.get(diff.change_type, diff.change_type)
            file_path = diff.b_path or diff.a_path
            output.append(f"\nFile: {file_path} | Change: {change_type}")

            try:
                if diff.a_blob and diff.b_blob:
                    # Modified file
                    a = diff.a_blob.data_stream.read().decode("utf-8", errors="ignore").splitlines()
                    b = diff.b_blob.data_stream.read().decode("utf-8", errors="ignore").splitlines()
                    udiff = unified_diff(a, b, fromfile="a/" + file_path, tofile="b/" + file_path, lineterm="")
                    output.extend(udiff)

                elif diff.b_blob:  # Added file
                    content = diff.b_blob.data_stream.read().decode("utf-8", errors="ignore")
                    output.append(f"\nAdded content:\n{content}")

                elif diff.a_blob:  # Deleted file
                    content = diff.a_blob.data_stream.read().decode("utf-8", errors="ignore")
                    output.append(f"\nDeleted content:\n{content}")
            except Exception as e:
                output.append(f"\nError reading file diff: {e}")

    return True, "\n".join(output)
