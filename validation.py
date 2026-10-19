from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import json

load_dotenv()

def validate_report(topic:str, sources:list[dict], report:str) -> dict:
    """evaluate report quality ans source coverage"""

    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        temperature=0,
        max_tokens=250
    )

    messages = [
        SystemMessage(content=(
            "you are a strict research quality reviewer" \
            "evaluate whether the report addresses the topic " \
            "contains meaningful findings and include source urls" \
            "do not assume that urls prove claims are correct" \
            "return exactly one JSON object with keys" \
            "'passed' (boolean) and 'feedback' (string)."
        )),
        HumanMessage(content=(
            f"topic {topic}\n"
            f"number of sources {len(sources)}\n"
            f"report \n {report}\n\n"
            "example format:" \
            "{'passed':true, 'feedback':'good coverage'}"
        ))
    ]

    try:
      response = llm.invoke(messages)

      result = json.loads(response.content)

      if not isinstance(result.get("passed"), bool):
        raise ValueError("Invalid passed field")

      if not isinstance(result.get("feedback"), str):
        raise ValueError("Invalid feedback field")

      return result

    except Exception as e:
      print("Validator error:", e)

      return {
        "passed": False,
        "feedback": "Validation failed due to an LLM or response error."}

    

   
    