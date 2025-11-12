import os
import json

class DocGenie:
    def __init__(self, repo_name: str, file_tree: list, readme_summary: str):
        self.repo_name = repo_name
        self.file_tree = file_tree
        self.readme_summary = readme_summary
        self.documentation = {}

    def generate_doc(self):
        """Generate a structured documentation dictionary"""
        self.documentation = {
            "repo_name": self.repo_name,
            "overview": self.readme_summary,
            "files": []
        }

        for item in self.file_tree:
            self.documentation["files"].append({
                "name": item["name"],
                "path": item["path"],
                "type": item.get("type", item.get("file_type", "unknown")),
                "size": item.get("size", None)
            })
        return self.documentation

    def save_doc(self, output_path="documentation.json"):
        """Save documentation as JSON"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.documentation, f, indent=2)
        print(f">>> Documentation saved to {output_path}")
