import os
import git
from git import InvalidGitRepositoryError, GitCommandError


def push_git():
    github_repo_url = 'https://github.com/mitch-palczewski/mitch-palczewski.github.io.git'
    
    try:
        repo = git.Repo('.', search_parent_directories=True)
    except InvalidGitRepositoryError:
        print("No git repository found. Initializing a new repository...")
        repo = git.Repo.init(os.getcwd())
        repo.create_remote('origin', github_repo_url)

    repo.git.add('--all') 

    try:
        repo.index.commit('Automated commit')
    except Exception as e:
        print("Commit failed (perhaps no changes?):", e)
    
    try:
        origin = repo.remote(name='origin')
    except ValueError:
        print("Remote 'origin' doesn't exist. Creating it...")
        origin = repo.create_remote('origin', github_repo_url)
    
    try:
        origin.push()
        print("Changes pushed successfully!")
    except GitCommandError as e:
        print("Failed to push changes. There might be an issue with the remote URL or repository configuration:", e)
