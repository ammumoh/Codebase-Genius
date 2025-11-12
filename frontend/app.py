import streamlit as st

st.title("Agentic Codebase Genius")
st.subheader("AI-Powered Code Documentation Generator")

uploaded_file = st.file_uploader("Upload your code file", type=['py', 'js', 'java'])
if uploaded_file:
    content = uploaded_file.read().decode()
    st.code(content, language='python')

    if st.button("Generate Documentation"):
        st.success("Documentation generated!")
        st.markdown(f"```text\n{content}\n```")
