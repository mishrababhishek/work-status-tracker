from setup_environment import setup_env
from get_diff import get_git_changes_today

import os

import constants as const

setup_env()

if __name__ == "__main__":
    repo_path = os.getenv(const.repo_path, None)
    repo_branch = os.getenv(const.repo_branch, None)
    if repo_path is None or len(repo_path) <= 0:
        print("Error: PYTHON_REPO_PATH environment variable is not set or is empty.")
        exit(1)
    if not os.path.exists(repo_path):
        print(f"Error: The repository path '{repo_path}' does not exist.")
        exit(1)
    if repo_branch is None or len(repo_branch) <= 0:
        print("Error: PYTHON_REPO_BRANCH environment variable is not set or is empty.")
        exit(1)
        
    print("Fetching today's git changes...")
    has_changes, changes = get_git_changes_today(repo_path, branch=os.getenv(const.repo_branch))
    if has_changes:
        print("Today's changes:")
        print(changes)
    else:
        print("No changes found for today.")