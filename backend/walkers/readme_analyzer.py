import os

class ReadmeAnalyzer:
    def __init__(self, file_tree, repo_path):
        self.file_tree = file_tree
        self.repo_path = repo_path
        self.summary = ""

    def analyze_readme(self):
        readmes = [f for f in self.file_tree if f["type"] == "file" and f["name"].lower().startswith("readme")]
        if not readmes:
            self.summary = "No README found"
            return self.summary

        readme_path = os.path.join(self.repo_path, readmes[0]["path"])
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.summary = f"README found ({len(content)} chars). Preview: {content[:200]}..."
        except Exception as e:
            self.summary = f"Error reading README: {e}"
        return self.summary

