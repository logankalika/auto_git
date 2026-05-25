import subprocess
from datetime import datetime
from pathlib import Path
import configparser

# File paths relative to the script location
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.ini"
COMMIT_FILE = BASE_DIR / "holy_commits.txt"

def first_time_setup():
    """Prompts the user for details and creates the config file if missing."""
    if CONFIG_FILE.exists():
        return

    print("--- First Time Setup ---")
    username = input("Enter your GitHub username: ").strip()
    token = input("Enter your GitHub Personal Access Token (PAT): ").strip()
    repo_url = input("Enter your GitHub repository link: ").strip()

    config = configparser.ConfigParser()
    config['github'] = {
        'username': username,
        'token': token,
        'repo_url': repo_url
    }

    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    # Secure the file immediately
    CONFIG_FILE.chmod(0o600)
    print(f"Setup complete! Settings saved securely to {CONFIG_FILE}\n")

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return {
        'username': config['github']['username'],
        'password': config['github']['token'],
        'repo_url': config['github']['repo_url']
    }

def auto_write():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(COMMIT_FILE, "a") as f:
        f.write(f"Commit at: {dt_string}\n")
    return dt_string

def terminal_git_commands(dt_string, cfg):
    git_username = cfg['username']
    git_password = cfg['password']
    git_repo = cfg['repo_url'].split("/")[-1].replace(".git", "")
    
    try:
        subprocess.run(["git", "init"], check=True, cwd=BASE_DIR)
        subprocess.run(["git", "add", "."], check=True, cwd=BASE_DIR)
        subprocess.run(["git", "commit", "-m", f"Commit at {dt_string}"], check=True, cwd=BASE_DIR)
        
        remote_url = f"https://{git_username}:{git_password}@://github.com{git_username}/{git_repo}.git"
        
        remotes = subprocess.run(["git", "remote"], capture_output=True, text=True, cwd=BASE_DIR).stdout
        if "origin" in remotes:
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True, cwd=BASE_DIR)
        else:
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True, cwd=BASE_DIR)
            
        subprocess.run(["git", "branch", "-M", "main"], check=True, cwd=BASE_DIR)
        subprocess.run(["git", "push", "-f", "-u", "origin", "main"], check=True, cwd=BASE_DIR)
        print(f"Successfully pushed: {dt_string}")
    except subprocess.CalledProcessError as e:
        print(f"Error during git commands: {e}")

def main():
    # Runs interactively if config.ini doesn't exist, otherwise skips it entirely
    first_time_setup()
    
    cfg = load_config()
    timestamp = auto_write()
    terminal_git_commands(timestamp, cfg)

if __name__ == "__main__":
    main()
