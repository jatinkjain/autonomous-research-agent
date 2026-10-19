import os 
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def research_topic(topic :str,instructions:str="") -> list[dict]:
    """Search the Web and return structured research sources."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing")

    if not topic.strip():
        raise ValueError("Reasearch topic cannot be empty.")

    client = TavilyClient(api_key= api_key)

    query= f"{topic}. additional research focus: {instructions}"

    try:
        response = client.search(
                query= query,
                search_depth="advanced" if instructions else "basic",
                max_results=5
            )
    except Exception as e:
        raise RuntimeError(f"Research search failed: {e}")    


    sources = []

    for result in response.get("results",[]):
        sources.append({
            "title":result.get("title",""),
            "url":result.get("url",""),
            "content":result.get("content","")
        })

    return sources
      