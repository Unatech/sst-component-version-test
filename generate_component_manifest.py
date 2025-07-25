import subprocess
import json
import os
import argparse

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Generate component manifest from latest Git commit.")
parser.add_argument("component", help="Name of the component folder (e.g., componentX)")
args = parser.parse_args()

# --- CONFIG ---
component_name = args.component
component_path = f"{component_name}/"
repo_url = "https://github.com/Unatech/sst-component-version-test.git"
#manifest_path = os.path.join(component_path, "component-manifest.json")  #put it in the config managed folder
manifest_path = os.path.join(os.path.dirname(__file__), f"{component_name}-manifest.json")


# --- Get last commit touching the component folder ---
print(f"Finding latest commit for folder: {component_path}")
result = subprocess.run(
    ["git", "log", "-n", "1", "--pretty=format:%H", "--", component_path],
    capture_output=True,
    text=True,
    check=True
)
commit_sha = result.stdout.strip()
print(f"Latest commit SHA: {commit_sha}")

# --- Write manifest ---
manifest = {
    "component": component_name,
    "version": "1",  #replace this with an identifier provided by the SST command line
    "repo": repo_url,
    "git_commit": commit_sha,
    "git_tag": "",  # optional
    "path": component_path
}

with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest written to: {manifest_path}")

