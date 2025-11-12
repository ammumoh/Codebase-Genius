import json
from walkers.repo_mapper import RepoMapper
from walkers.readme_analyzer import ReadmeAnalyzer
from walkers.code_analyzer import CodeAnalyzer

if __name__ == "__main__":
    github_url = "https://github.com/REN-100/Generative-AI.git"
    
    # Step 1: Clone repo
    mapper = RepoMapper()
    if not mapper.clone_repository(github_url):
        exit(1)

    # Step 2: Generate file tree
    if not mapper.generate_file_tree():
        exit(1)

    # Step 3: Analyze README
    readme_analyzer = ReadmeAnalyzer(mapper.file_tree, mapper.local_path)
    readme_summary = readme_analyzer.analyze_readme()

    # Step 4: Analyze Python code
    code_analyzer = CodeAnalyzer(mapper.file_tree, mapper.local_path)
    code_summary = code_analyzer.analyze_python_files()

    # Step 5: Combine results
    result = {
        "repo_name": mapper.repo_name,
        "file_count": len(mapper.file_tree),
        "readme_summary": readme_summary,
        "code_summary": code_summary[:5],  # show first 5 files for preview
        "file_tree_sample": mapper.file_tree[:10]
    }

    print(json.dumps(result, indent=2))
