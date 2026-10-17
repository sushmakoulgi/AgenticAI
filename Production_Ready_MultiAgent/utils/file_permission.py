from pathlib import Path


DOCUMENT_FOLDER=Path("documents").resolve()

def safe_file_path(filename):
    path=Path(f"Documents\{filename}").resolve()

    if not path.is_relative_to(DOCUMENT_FOLDER):
        raise PermissionError("File is not Accessible: ACCESS DENIED")
    
    return path