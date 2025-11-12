walker RepoMapper;

has repo_path as string;
has file_list as list;

can map_repository with entry {
    print(f"Scanning repository at: {self.repo_path}");
    
    # Python interop one-liners
    py_stmt "import os";
    py_stmt "files = []";
    py_stmt "[(files.append(f'{dirpath}/{f}')) for dirpath, dirnames, filenames in os.walk(self.repo_path) for f in filenames]";
    py_stmt "self.file_list = files";
    
    print(f"Found {len(self.file_list)} files");
};
