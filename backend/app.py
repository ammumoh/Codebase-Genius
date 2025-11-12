import streamlit as st
import json
from walkers.repo_mapper import RepoMapper
from walkers.readme_analyzer import ReadmeAnalyzer
from walkers.code_analyzer import CodeAnalyzer

st.set_page_config(
    page_title="Codebase Genius 🧠",
    layout="wide",
    page_icon="🧩"
)

st.title("🧠 Codebase Genius — Multi-Agent Repo Analyzer")

st.write("""
Welcome to **Codebase Genius** — an AI-powered codebase analyzer that automatically documents and inspects any GitHub repo.
Just paste a repo URL below and let the system do the work!
""")

# --- Sidebar input ---
st.sidebar.header("Repository Settings")
github_url = st.sidebar.text_input(
    "Enter GitHub repository URL",
    "https://github.com/REN-100/Generative-AI.git"
)

analyze_btn = st.sidebar.button("🚀 Analyze Repository")

# --- Run analysis when button clicked ---
if analyze_btn:
    st.subheader("⚙️ Running Codebase Genius Pipeline...")

    # Step 1: Clone repo
    mapper = RepoMapper()
    with st.spinner("Cloning or updating repository..."):
        if not mapper.clone_repository(github_url):
            st.error(f"Error cloning repository: {mapper.error}")
            st.stop()

    # Step 2: Generate file tree
    with st.spinner("Mapping repository files..."):
        if not mapper.generate_file_tree():
            st.error(f"Error generating file tree: {mapper.error}")
            st.stop()

    # Step 3: Analyze README
    with st.spinner("Analyzing README file..."):
        readme_analyzer = ReadmeAnalyzer(mapper.file_tree, mapper.local_path)
        readme_summary = readme_analyzer.analyze_readme()

    # Step 4: Analyze Python files
    with st.spinner("Scanning Python code files..."):
        code_analyzer = CodeAnalyzer(mapper.file_tree, mapper.local_path)
        code_summary = code_analyzer.analyze_python_files()

    # --- Display results ---
    st.success("✅ Analysis Complete!")

    repo_info = {
        "Repository Name": mapper.repo_name,
        "Total Files": len(mapper.file_tree),
        "Local Path": mapper.local_path
    }

    st.subheader("📦 Repository Info")
    st.json(repo_info)

    st.subheader("📘 README Summary")
    st.text_area("Preview", readme_summary, height=200)

    st.subheader("🧮 File Tree Sample")
    st.dataframe(mapper.file_tree[:20])

    st.subheader("🐍 Python Code Analysis (first few files)")
    for f in code_summary[:5]:
        with st.expander(f"📄 {f['file']}"):
            if "error" in f:
                st.error(f"Error reading: {f['error']}")
            else:
                st.code(f["preview"], language="python")

    # --- Optional download ---
    result_json = {
        "repo_name": mapper.repo_name,
        "file_count": len(mapper.file_tree),
        "readme_summary": readme_summary,
        "file_tree_sample": mapper.file_tree[:10],
        "code_summary": code_summary[:5],
    }

    st.download_button(
        label="⬇️ Download Analysis JSON",
        data=json.dumps(result_json, indent=2),
        file_name=f"{mapper.repo_name}_analysis.json",
        mime="application/json"
    )

else:
    st.info("👈 Enter a GitHub repository in the sidebar and click 'Analyze Repository' to start.")

