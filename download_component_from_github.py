import os
import json
import requests

def download_folder(repo, commit, path, target_dir, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={commit}"

    print(f"📁 Downloading from: {url}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    items = response.json()
    os.makedirs(target_dir, exist_ok=True)

    for item in items:
        item_path = item["path"]
        if item["type"] == "file":
            download_url = item["download_url"]
            local_path = os.path.join(target_dir, os.path.relpath(item_path, path))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            print(f"📄 Downloading file: {item_path}")
            file_resp = requests.get(download_url, headers=headers)
            file_resp.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(file_resp.content)

        elif item["type"] == "dir":
            download_folder(repo, commit, item_path, os.path.join(target_dir, os.path.basename(item_path)), token)

# --- Load manifest ---
with open("component-manifest.json", "r") as f:
    manifest = json.load(f)

repo_url = manifest["repo"]
repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
commit = manifest["git_commit"]
path = manifest["path"].strip("/")
target_dir = f"build_workspace/{manifest['component']}"

# Optional GitHub token for private repos or rate limits
github_token = None  # set to your token string if needed

download_folder(repo=repo_name, commit=commit, path=path, target_dir=target_dir, token=github_token)

print(f"✅ Component restored to: {target_dir}")
