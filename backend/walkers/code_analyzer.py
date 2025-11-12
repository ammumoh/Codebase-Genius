# walkers/code_analyzer.py
import os

class CodeAnalyzer:
    def __init__(self, file_tree, base_path):
        self.file_tree = file_tree
        self.base_path = base_path
        self.analysis = []

    def analyze_python_files(self):
        for f in self.file_tree:
            if f["type"] == "file" and f["name"].endswith(".py"):
                try:
                    file_path = os.path.join(self.base_path, f["path"])
                    with open(file_path, "r", encoding="utf-8") as fp:
                        content = fp.read()
                    # very simple: store first 200 chars of code
                    self.analysis.append({
                        "file": f["path"],
                        "preview": content[:200]
                    })
                except Exception as e:
                    self.analysis.append({
                        "file": f["path"],
                        "error": str(e)
                    })
        return self.analysis
