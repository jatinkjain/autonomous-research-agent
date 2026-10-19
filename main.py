from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from pathlib import Path
from datetime import datetime

from researcher import research_topic
from writer import write_report
from validation import validate_report



class ReasearchState(TypedDict):
    topic:str
    sources:list[dict]
    report:str
    validation_passed:bool
    feedback:str
    research_instructions:str
    retry_count:int
    seen_urls:list[str]



def reasearcher_node(state: ReasearchState) -> dict:
    new_sources = research_topic(
        state["topic"],
        state["research_instructions"]
    )

    if not new_sources:
      return {
        "sources": state["sources"],
        "feedback": "No new sources found. Try a more specific search query."
    }

    # Normalize existing sources into dictionaries
    existing_sources = []
    for source in state["sources"]:
        if isinstance(source, dict):
            existing_sources.append(source)

    seen_urls = {
        source["url"]
        for source in existing_sources
        if source.get("url")
    }

    unique_sources = []

    for source in new_sources:
        url = source.get("url", "").strip()

        if url and url not in seen_urls:
            unique_sources.append(source)
            seen_urls.add(url)

    all_sources = existing_sources + unique_sources

    return {
        "sources": all_sources,
        "seen_urls": list(seen_urls)
    }

def writer_node(state: ReasearchState)-> dict:

    report = write_report(state["topic"],state["sources"])

    return{"report":report}

def validator_node(state: ReasearchState)-> dict:
    result = validate_report(state["topic"],state["sources"],state["report"])

    return {"validation_passed":result["passed"],
            "feedback":result["feedback"]}

def route_after_validation(state:ReasearchState)-> str:
    if state["validation_passed"]:
        return "end"

    if state["retry_count"] < 1:
        return "retry"

    return "end"

def retry_node(state:ReasearchState)-> dict:
    print("\n validation failed. retrying research...")
    print("Feedback:", state["feedback"])

    return {"retry_count":state["retry_count"] + 1,
            "research_instructions":(
                "improve the previous research."
                "address this validatior feedback"
                f"{state['feedback']}"
                "look for additional evidence and different sources."
                "avoid repeating the same findings"
            ) }

def save_report(topic:str,report:str)-> str:
    reports_dir= Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = reports_dir / f"research_{timestamp}.md"

    content = f"""# Research Report

**Topic:** {topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{report}
"""

    file_path.write_text(content, encoding="utf-8")
    return str(file_path)




builder = StateGraph(ReasearchState)
builder.add_node("researcher",reasearcher_node)
builder.add_node("writer",writer_node)
builder.add_node("validator",validator_node)
builder.add_node("retry",retry_node)

builder.add_edge(START,"researcher")
builder.add_edge("researcher","writer")
builder.add_edge("writer","validator")
builder.add_conditional_edges("validator",route_after_validation,{
    "end":END,"retry":"retry"
})
builder.add_edge("retry","researcher")

with SqliteSaver.from_conn_string(
    "research_checkpoints.sqlite"
) as checkpointer:

    research_graph = builder.compile(
        checkpointer=checkpointer
    )

    topic = input("Enter your research topic: ").strip()

    if not topic:
        print("please enter a valid topic.")

    else :   
        config = {
                "configurable": {
                    "thread_id": "research-session-002"
                }
            }
        
        snapshot = research_graph.get_state(config)
        
        result = research_graph.invoke(
                {
                    "topic": topic,
                    "sources": [],
                    "report": "",
                    "validation_passed": False,
                    "feedback": "",
                    "retry_count": 0,
                    "research_instructions": "",
                    "seen_urls": []
                },
                config=config
            )

        print("Final Report: ",result["report"])

        if result["report"]:
          saved_path = save_report(
          result["topic"],
          result["report"])

        print(f"\nReport saved to: {saved_path}")
        
    