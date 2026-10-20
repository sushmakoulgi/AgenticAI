import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, quote
from xml.etree import ElementTree
import json
from llm import ClaudeLLM

HEADERS = {
    "User-Agent": (
        "ResearchAIAgent/1.0 "
        "(educational project)"
    )
}

research_notes=[]


def search_wikipedia(query, max_results=5):
    """
    Search Wikipedia articles.

    Args:
        query: Search query.
        max_results: Maximum number of results.

    Returns:
        A list of search results.
    """

    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": max_results,
            "format": "json"
        },
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    results = []

    for result in response.json()["query"]["search"]:

        title = result["title"]

        results.append({
            "title": title,
            "url": (
                "https://en.wikipedia.org/wiki/"
                + quote(title.replace(" ", "_"))
            ),
            # Snippets contain HTML highlight tags
            "snippet": BeautifulSoup(
                result["snippet"],
                "html.parser"
            ).get_text()
        })

    return results


def search_arxiv(query, max_results=5):
    """
    Search arXiv research papers.

    Args:
        query: Search query.
        max_results: Maximum number of results.

    Returns:
        A list of search results.
    """

    response = requests.get(
        "https://export.arxiv.org/api/query",
        params={
            "search_query": f"all:{query}",
            "max_results": max_results
        },
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    root = ElementTree.fromstring(response.text)

    results = []

    for entry in root.findall(
        "atom:entry",
        namespace
    ):

        results.append({
            "title": " ".join(
                entry.findtext(
                    "atom:title",
                    "",
                    namespace
                ).split()
            ),
            "url": entry.findtext(
                "atom:id",
                "",
                namespace
            ),
            "snippet": " ".join(
                entry.findtext(
                    "atom:summary",
                    "",
                    namespace
                ).split()
            )
        })

    return results


def search_web(query, max_results=2):
    """
    Search Wikipedia and arXiv.

    Args:
        query: Search query.
        max_results: Maximum results per source.

    Returns:
        A list of search results.
    """

    return (
        search_wikipedia(query, max_results)
        # + search_arxiv(query, max_results)
    )


def read_webpage(url):
    """
    Download a webpage and extract its text.

    Args:
        url: Webpage URL.

    Returns:
        Extracted webpage text.
    """


    if url.startswith("//"):
        url = "https:" + url

    # Extract the real URL from 
    #  DuckDuckGo redirect URL
    parsed_url = urlparse(url)

    if "duckduckgo.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)

        if "uddg" in params:
            url = params["uddg"][0]
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    text = soup.get_text(
        "\n",
        strip=True
    )

    return text[:12000]

def add_research_notes(source, findings, evidence):
    """
    add the source of webpage url and what are the findings from the webpage (source)
    and associated evidence
    args: source(url)
    findings :research findings
    evidence: evidence of this finding
    
    returns : if research is successfully added and also the associated finding"""

    research_notes.append({
        "source":source,
        "findings":findings,
        "evidence":evidence,
        "verified":False
    })

    return {
        "response":"added",
        "verified":False,
        "findings":findings
    }


def get_research_notes():
    """ return all the research notes collected so far 
    returns all the notes in a list""
    """
    notes=[] 
    for note in research_notes:
        notes.append(note.copy())
    return notes

def mark_finding_verified(source, findings):
    for note in research_notes:
        if note["source"]==source and note["findings"]==findings:
            note["verified"]=True
            return {
                "verified":True,
                "findings":findings,
                "source":source
            }

    return {
                    "verified":False,
                    "findings":findings,
                    "source":source
                }

def get_verified_research_notes():
    """ return all the research notes collected so far 
    returns all the notes in a list""
    """
    notes=[] 
    for note in research_notes:
        if note["verified"]==True:
            notes.append(note.copy())
    return notes

async def verify_findings(
        source,findings,evidence
):
    """Verify whether evidence mathes the findings"""
    llm=ClaudeLLM()
    system="you are an AI evidence evalautor, for a given findings check if the provided envidence is supporting" \
    " return only json, for example {\"supported\": true, \"explanation\": \"short one liner\"}"
    message=[{
        "role":"user",
        "content":f" verify the findings {findings} against evidence {evidence} based on the source {source} "
    }]
    raw_response=await llm.generate_raw_response(messages=message,system=system)
    await llm.close()
    text="".join(block.text for block in raw_response.content if block.type=="text")
    # Claude sometimes wraps the json in ```json fences; keep just the {...} part
    result=json.loads(text[text.find("{"):text.rfind("}")+1])
    if result["supported"]== True:
        mark_finding_verified(source,findings)
    return result
    
async def generate_report(user_request, verified_findings):
    research_text=""
    for item in verified_findings:
        research_text+=item["source"]+ "\n" +item["evidence"]+"\n"+item["findings"]+"\n"

    prompt=[{ "role":"user","content":
        f"you are an AI report generator, given the user request {user_request} and the research text {research_text} generate report explaining header, sources used, evidences available, and paragraph on the research topic"
    }]
    llm=ClaudeLLM()
    raw_response=await llm.generate_raw_response(prompt)
    await llm.close()
    return "".join(
                        block.text for block in raw_response.content if block.type == "text"
                    )


search_web_tool = {
    "name": "search_web",
    "description": """Search Wikipedia and arXiv.
    
        Args:
            query: Search query.
            max_results: Maximum results per source.
    
        Returns:
            A list of search results.""",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "User query to search"
            },
            "max_results":{
                "type": "integer",
                "description":"max number of results from web search"
            }
        },
        "required": ["query"]
    }
}

read_web_page_tool={
    "name": "read_webpage",
    "description": """Downloads the given url from web
    
        Args:
            url: URL of the webpage to download.
           
        Returns:
            content of the webpage""",
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "web page url "
            }
        },
        "required": ["url"]
    }
}

add_research_notes_tool={
    "name": "add_research_notes",
    "description": """add the source of webpage url and what are the findings from the webpage (source)
        and associated evidence
        args: source(url)
        findings :research findings
        evidence: evidence of this finding
        
        returns : if research is successfully added and also the associated finding""",
    "input_schema": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "web page url "
            },
            "findings":
            {
                "type": "string",
                "description": "web page findings on the research "
            },
            "evidence":
            {
                "type": "string",
                "description": "Evidence of the research "
            }
        },
        "required": ["source","findings","evidence"]
    }
}


get_research_notes_tool={
    "name": "get_research_notes",
    "description":   """ return all the research notes collected so far 
        returns all the notes in a list""
        """,
    "input_schema": {"type": "object",
        "properties": {}  # Empty properties object,
    }
    
    }

verify_findings_tool={
    "name": "verify_findings",
    "description": """Verify whether evidence mathes the findings""",
    "input_schema": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "web page url "
            },
            "findings":
            {
                "type": "string",
                "description": "web page findings on the research "
            },
            "evidence":
            {
                "type": "string",
                "description": "Evidence of the research "
            }
        },
        "required": ["source","findings","evidence"]
    }
}

