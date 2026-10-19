import os 
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,SystemMessage

load_dotenv()

def write_report(topic:str, sources:list[dict])-> str:
    """Generate a research report using collected web sources."""

    if not sources:
        return "unable to generate a report: no research sources found."

    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=0,
        max_tokens=700
    )

    research_material = "\n\n".join(
        f"source:{source['title']}\n"
        f"url:{source['url']}\n"
        f"content:{source['content']}"
        for source in sources
    )

    message = [
        SystemMessage(content= (
            "you are a research report writer. "
            "use the supplied research material to write a clear structured report. "
            "do not invent facts or citations. if evidence is insufficient, say so. "
            "include source urls next to releveant findings."
        )),
        HumanMessage(content=(
            f"Research topic: {topic}\n\n"
            f"Research material\n: {research_material}\n\n"
            "write a report with these sections:\n" \
            "1. exectutive summary\n" \
            "2. key findings\n" \
            "3. analysis \n" \
            "4. limitations\n" \
            "5. sources"
            "keep the report under 500 words. include relevant source urls."
        ))
    ]

    try:
        response = llm.invoke(message)
        return response.content
    except Exception as e :
        print(f"writer LLM error {e}")
        return (
            "Report generation failed because the LLM request "
        "could not be completed. Please try again."
        )

    


