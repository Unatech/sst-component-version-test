import json
import os
import shutil
import subprocess

# Load manifest
with open("componentX/component-manifest.json", "r") as f:
    manifest = json.load(f)

repo_url = "https://github.com/Unatech/sst-component-version-test.git"  # replace if using different URL
commit = manifest["git_commit"]
folder_path = manifest["path"].rstrip("/")
component = manifest["component"]

# Target workspace folder
workspace_folder = f"build_workspace/{component}"

# Step 1: Clone into temp folder
clone_dir = "_tmp_repo"

if os.path.exists(clone_dir):
    shutil.rmtree(clone_dir)

print(f"Cloning repo into {clone_dir}...")
subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

# Step 2: Checkout to exact commit
os.chdir(clone_dir)
print(f"Checking out commit {commit}...")
subprocess.run(["git", "checkout", commit], check=True)

# Step 3: Copy the component folder to the build workspace
os.chdir("..")
if os.path.exists(workspace_folder):
    shutil.rmtree(workspace_folder)

print(f"Copying {folder_path} → {workspace_folder}")
shutil.copytree(os.path.join(clone_dir, folder_path), workspace_folder)

# Step 4: Cleanup temp repo
#shutil.rmtree(clone_dir)
print("✅ Component restored to:", workspace_folder)
