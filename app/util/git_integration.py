import git
import os

from config import get_project_path

def push_git():
    repo = git.Repo('.', search_parent_directories=True)
    repo_path = repo.working_tree_dir
    repo = git.Repo(repo_path)
    repo.git.add('--all')  # Add all changes
    repo.index.commit('Automated commit')  # Commit changes
    origin = repo.remote(name='origin')
    origin.push()  # Push to GitHub
    print("Changes pushed successfully!")


push_git()