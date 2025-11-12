import os
import git

class RepoMapper:
    def __init__(self):
        self.repo_name = ""
        self.local_path = ""
        self.file_tree = []
        self.error = ""
        self.readme_summary = ""

    def clone_repository(self, github_url: str) -> bool:
        try:
            print(f">>> Cloning repository: {github_url}")
            self.repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")
            self.local_path = f"./temp_repos/{self.repo_name}"
            os.makedirs("./temp_repos", exist_ok=True)

            if os.path.exists(self.local_path) and os.listdir(self.local_path):
                print(f">>> Repository already exists at {self.local_path}, skipping clone.")
                return True

            git.Repo.clone_from(github_url, self.local_path)
            print(f">>> Successfully cloned to {self.local_path}")
            return True
        except Exception as e:
            self.error = str(e)
            print(f">>> ERROR: {self.error}")
            return False

    def generate_file_tree(self) -> bool:
        try:
            self.file_tree = []
            for root, dirs, files in os.walk(self.local_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

                # Add directories
                for d in dirs:
                    dir_path = os.path.join(root, d)
                    self.file_tree.append({
                        "name": d,
                        "path": os.path.relpath(dir_path, self.local_path),
                        "type": "dir"
                    })

                # Add files
                for f in files:
                    file_path = os.path.join(root, f)
                    self.file_tree.append({
                        "name": f,
                        "path": os.path.relpath(file_path, self.local_path),
                        "type": "file",
                        "size": os.path.getsize(file_path)
                    })
            print(f">>> File tree generated: {len(self.file_tree)} items")
            return True
        except Exception as e:
            self.error = str(e)
            print(f">>> ERROR: {self.error}")
            return False

    def analyze_readme(self):
        """Find the first README and summarize"""
        for f in self.file_tree:
            if f["type"] == "file" and f["name"].lower().startswith("readme"):
                readme_path = os.path.join(self.local_path, f["path"])
                try:
                    with open(readme_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.readme_summary = f"README found ({len(content)} chars). Preview: {content[:200]}..."
                        return self.readme_summary
                except Exception as e:
                    self.readme_summary = f"Error reading README: {e}"
                    return self.readme_summary
        self.readme_summary = "No README found"
        return self.readme_summary
