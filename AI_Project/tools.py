import re
from pathlib import Path
from langchain_core.tools import tool

CONTEXT_DIR=Path(__file__).resolve().parent/"context"
MAPPING_FILE=CONTEXT_DIR/"mapping.txt"

# Notes collected by add_research_notes
research_notes=[]

# Share of a note's key words that must appear in the source file
VERIFY_THRESHOLD=0.6
STOP_WORDS={
    "the","and","for","are","was","were","that","this","with","from","into","its","has",
    "have","had","can","which","such","use","used","uses","using","also","their","they",
    "them","than","then","each","other","more","most","many","one","two","not","but",
    "all","any","you","your","how","what","when","where","who","why","about","like",
}


def load_mapping():
    """Read mapping.txt and return a dict of keyword -> file name."""
    mapping={}
    for line in MAPPING_FILE.read_text().splitlines():
        line=line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        keywords,file_name=line.rsplit(":",1)
        for keyword in keywords.split(","):
            mapping[keyword.strip().lower()]=file_name.strip()
    return mapping


@tool
def search_web(query:str) -> str:
    """Find which files contain information about the query (MCP or Python topics).
    Returns the file names. Call read_web_page with a file name to get its content."""
    mapping=load_mapping()
    query=query.lower()

    matched_files=[]
    for keyword,file_name in mapping.items():
        if keyword in query and file_name not in matched_files:
            matched_files.append(file_name)

    if not matched_files:
        topics=", ".join(sorted(mapping))
        return f"No files found for '{query}'. Available topics: {topics}"

    return "Relevant files: "+", ".join(matched_files)


def read_context_file(file_name):
    """Return the text of a file in the context folder, or None if it is not allowed or missing."""
    file_path=(CONTEXT_DIR/file_name.strip()).resolve()

    # Only allow files directly inside the context folder
    if file_path.parent!=CONTEXT_DIR or file_path.name=="mapping.txt":
        return None
    if not file_path.is_file():
        return None
    return file_path.read_text()


def key_words(text):
    """Lowercase words of 3+ letters, without common stop words."""
    words=re.findall(r"[a-z0-9]+",text.lower())
    return {w for w in words if len(w)>=3 and w not in STOP_WORDS}


@tool
def read_web_page(file_name:str) -> str:
    """Read a file from the context folder and return its content.
    Use a file name returned by search_web, for example 'mcp.txt'."""
    content=read_context_file(file_name)
    if content is None:
        return f"File '{file_name}' not found in the context folder."
    return content


@tool
def add_research_notes(source:str,findings:str) -> str:
    """Save key findings from a file read with read_web_page.
    source is the file name (for example 'mcp.txt') and findings is a short summary
    of the important points from that file."""
    if not source.strip() or not findings.strip():
        return "Both source and findings are required."

    research_notes.append({
        "source":source.strip(),
        "findings":findings.strip(),
        "verified":False
    })
    return f"Note saved from {source}. Total notes: {len(research_notes)}"


@tool
def verify_research_notes(source:str,findings:str) -> str:
    """Check that saved findings are supported by their source file, and mark the note verified.
    Pass the same source and findings that were given to add_research_notes."""
    source=source.strip()
    findings=findings.strip()

    note=None
    for saved in research_notes:
        if saved["source"]==source and saved["findings"]==findings:
            note=saved
            break
    if note is None:
        return f"No saved note found from {source} with these findings. Save it with add_research_notes first."

    content=read_context_file(source)
    if content is None:
        return f"Source '{source}' not found in the context folder, so the note cannot be verified."

    finding_words=key_words(findings)
    if not finding_words:
        return "Findings have no key words to check."

    matched=finding_words & key_words(content)
    score=len(matched)/len(finding_words)
    note["verified"]=score>=VERIFY_THRESHOLD

    if note["verified"]:
        return f"Verified: {score:.0%} of the key words in the findings appear in {source}."
    missing=", ".join(sorted(finding_words-matched))
    return (f"Not verified: only {score:.0%} of the key words appear in {source}. "
            f"Not found in source: {missing}")


@tool
def get_verified_notes() -> str:
    """Return all research notes that have been verified.
    Use these notes to write the final research answer."""
    verified=[note for note in research_notes if note["verified"]]
    if not verified:
        return "No verified notes yet."

    lines=[f"{i}. [{note['source']}] {note['findings']}" for i,note in enumerate(verified,1)]
    return "\n".join(lines)
