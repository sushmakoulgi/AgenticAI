from model import model
from tenacity import retry,wait_exponential,stop_after_attempt
import asyncio
import html
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException
from langchain_core.messages import SystemMessage,HumanMessage,ToolMessage
from research_schemas import ResearchPlan,ResearchReport
from tools import search_web,read_web_page,add_research_notes,verify_research_notes,get_verified_notes,research_notes

# Research agent stops after this many LLM calls, even if it is not finished
MAX_STEPS=10

TOOLS=[search_web,read_web_page,add_research_notes,verify_research_notes,get_verified_notes]
TOOLS_BY_NAME={t.name:t for t in TOOLS}

REPORTS_DIR=Path(__file__).resolve().parent/"reports"


# ---------- Planning agent ----------

PLANNER_PROMPT="""You plan research for an agent. Break the user's request into exactly 3 main tasks,
in the order the agent should do them. Each task is one short sentence.
The agent can only use these tools: search_web (find relevant files), read_web_page (read a file),
add_research_notes (save findings), verify_research_notes (check findings against the source)
and get_verified_notes (fetch verified notes). The tools only work on local files in the
context folder, not the internet, so do not plan to visit websites, docs or GitHub."""

planner=model.with_structured_output(ResearchPlan,method="json_schema")


async def plan_research(request):
    """LLM call that returns a list of 3 tasks for the agent to complete the request."""
    plan=await planner.ainvoke([
        {"role":"system","content":PLANNER_PROMPT},
        {"role":"user","content":request}
    ])
    return plan.tasks


# ---------- Research agent ----------

RESEARCH_PROMPT="""You are a research agent. Follow the research plan you are given, using only the
files in the context folder, never your own knowledge. Use the tools in this order:

1. search_web: find which files are relevant to the topic.
2. read_web_page: read each relevant file.
3. add_research_notes: save the key findings from each file, with the file name as the source.
4. verify_research_notes: verify each saved note, using exactly the same source and findings.
5. get_verified_notes: fetch the verified notes. This is the last step.

Do not write a report. Another agent writes the report from the verified notes."""

researcher=model.bind_tools(TOOLS)


async def run_tool(tool_call):
    """Execute one tool call from the research agent and return the ToolMessage."""
    tool=TOOLS_BY_NAME.get(tool_call["name"])
    if tool is None:
        return ToolMessage(content=f"Unknown tool: {tool_call['name']}",tool_call_id=tool_call["id"])
    try:
        # Invoking a tool with the whole tool call returns a ToolMessage
        return await tool.ainvoke(tool_call)
    except Exception as exc:
        return ToolMessage(content=f"Tool {tool_call['name']} failed: {exc}",tool_call_id=tool_call["id"])


async def research_agent(request,tasks,callback):
    """Run the plan: call the LLM, execute any tool calls it returns, and send the results back.
    Stops when the verified notes are fetched, the LLM makes no more tool calls, or MAX_STEPS is reached.
    Returns the verified notes."""
    plan="\n".join(f"{i}. {task}" for i,task in enumerate(tasks,1))
    messages=[
        SystemMessage(content=RESEARCH_PROMPT),
        HumanMessage(content=f"User request: {request}\n\nResearch plan:\n{plan}")
    ]

    for step in range(1,MAX_STEPS+1):
        emit({
                    "type":"Research Step",
                    "message":f"Executing Research step {step} is complete ",
                    "output":f"step {step}"
                },callback)
        ai_message=await researcher.ainvoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            print(f"Step {step}: research agent made no tool call, research finished")
            emit({
                        "type":"Research Step",
                        "message":"Research plan is complete ",
                        "output":f"Step {step}: research agent made no tool call, research finished"
                    },callback)
            break

        for tool_call in ai_message.tool_calls:
            print(f"Step {step}: {tool_call['name']}({tool_call['args']})")
            emit({
                    "type":"Tool call Step",
                    "message":"Tool calling ",
                    "output":f"Step {step}: {tool_call['name']}({tool_call['args']})"
                },callback)
            messages.append(await run_tool(tool_call))
            emit({
                        "type":"Tool call Complete",
                        "message":"Tool call Complete ",
                        "output":f"Step {step}: {tool_call['name']}({tool_call['args']}) complete"
                    },callback)
        if any(call["name"]=="get_verified_notes" for call in ai_message.tool_calls):
            print(f"Step {step}: verified notes fetched, research complete")
            emit({
                    "type":"Verification Step",
                    "message":"Verifying Research Notes",
                    "output":f"Step {step}:  Research Verification"
                },callback)
            break
    else:
        print(f"Stopped after {MAX_STEPS} steps")
        emit({
                "type":"Stopping due to max steps",
                "message":"Max steps compelted ",
                "output":f"Step {step}: {tool_call['name']}({tool_call['args']})"
            },callback)

    return [note for note in research_notes if note["verified"]]


# ---------- Reporter agent ----------

REPORTER_PROMPT="""You are a reporter. Write a short research report for the user's request,
using only the verified findings you are given. Do not add facts that are not in the findings.
Give the report a heading, list what the research says (one item per finding, with its source file),
and end with a one-line summary."""

reporter=model.with_structured_output(ResearchReport,method="json_schema")


async def reporter_agent(request,notes,callback):
    """LLM call that turns the user request and verified notes into a plain-text report."""
    if not notes:
        report=ResearchReport(
            heading=request,
            findings=[],
            summary="No verified information was found for this request."
        )
    else:
        findings="\n".join(f"- [{note['source']}] {note['findings']}" for note in notes)
        report=await reporter.ainvoke([
            {"role":"system","content":REPORTER_PROMPT},
            {"role":"user","content":f"User request: {request}\n\nVerified findings:\n{findings}"}
        ])
    report_text=build_report_text(request,report)
    emit({
                "type":"Report",
                "message":"Research report is complete ",
                "output":report_text
            },callback)
    save_report(report.heading,build_report_html(request,report))
    return report_text


def build_report_text(request,report):
    """Build the report as plain text to return to the research API."""
    if report.findings:
        findings_text="\n".join(f"- {f.point} [{f.source}]" for f in report.findings)
    else:
        findings_text="No findings."

    return f"""{report.heading}

Request: {request}

What the research says
{findings_text}

Summary
{report.summary}"""


def build_report_html(request,report):
    """Build the report as an HTML fragment to show inline on the page. All text from the LLM is escaped."""
    e=html.escape
    if report.findings:
        items="\n".join(
            f'    <li>{e(f.point)} <span class="report-source">{e(f.source)}</span></li>'
            for f in report.findings
        )
        findings_html=f"<ul>\n{items}\n  </ul>"
    else:
        findings_html="<p>No findings.</p>"

    return f"""<article class="report">
  <h3 class="report-heading">{e(report.heading)}</h3>
  <p class="report-request">Request: {e(request)}</p>
  <h4>What the research says</h4>
  {findings_html}
  <h4>Summary</h4>
  <p class="report-summary">{e(report.summary)}</p>
</article>"""


# Styles for the saved report file (the web page uses the same rules from style.css)
REPORT_PAGE_CSS="""
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
       color: #1f2937; background: #f4f6fb; line-height: 1.6; margin: 0; padding: 2rem 1rem; }
.report { max-width: 760px; margin: 0 auto; background: #fff; border-radius: 12px; padding: 1.5rem;
          box-shadow: 0 4px 16px rgba(17, 24, 39, 0.08); }
.report-heading { color: #4f46e5; font-size: 1.4rem; margin: 0 0 0.25rem; }
.report-request { color: #6b7280; font-size: 0.9rem; margin: 0 0 1rem; }
.report h4 { font-size: 1.05rem; margin: 1.25rem 0 0.5rem; }
.report ul { padding-left: 1.25rem; margin: 0; }
.report li { margin-bottom: 0.5rem; }
.report-source { display: inline-block; font-size: 0.75rem; color: #4f46e5; background: #eef2ff;
                 border-radius: 4px; padding: 0 0.4rem; margin-left: 0.25rem; }
.report-summary { background: #f4f6fb; border-left: 4px solid #4f46e5; padding: 0.75rem 1rem;
                  border-radius: 4px; margin: 0; }
"""


def save_report(heading,report_html):
    """Save the report as a standalone HTML page in the reports folder."""
    page=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(heading)}</title>
<style>{REPORT_PAGE_CSS}</style>
</head>
<body>
{report_html}
</body>
</html>"""
    REPORTS_DIR.mkdir(exist_ok=True)
    file_path=REPORTS_DIR/f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
    file_path.write_text(page)
    print(f"Report saved to {file_path}")

def emit(message,progress_callback):
    if progress_callback:
        progress_callback(message)

# ---------- Orchestrator ----------

@retry(stop=stop_after_attempt(2),wait=wait_exponential(multiplier=1,min=1,max=4),reraise=True)
async def run_agent(request,callback):
    """Plan, research, then report. Returns the report as plain text."""
    # Start each request with an empty notes list
    research_notes.clear()
    try:
        tasks=await plan_research(request)
        print("Research plan:\n"+"\n".join(f"{i}. {task}" for i,task in enumerate(tasks,1)))
        emit({
            "type":"plan",
            "message":"Research plan is complete ",
            "output":tasks
        },callback)
        notes=await asyncio.wait_for(research_agent(request,tasks,callback),timeout=120)
        print(f"Verified notes: {len(notes)}")

        emit({
                    "type":"verification",
                    "message":"these are number of the verified notes ",
                    "output":len(notes)
                },callback)
        return await reporter_agent(request,notes,callback)
    except asyncio.TimeoutError as te:
        raise HTTPException(
            status_code=504,
            detail="request timed out"
        )
    except Exception as exc:
        print(f"Agent Execution Failed",exc)
        raise HTTPException(
            status_code=500,
            detail="Agent Execution Failed"
        )
