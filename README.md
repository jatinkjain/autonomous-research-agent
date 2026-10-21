# Autonomous Research Agent

An AI-powered research agent that searches the web, generates structured research reports, validates the output, and retries research when the report does not pass validation.


## Live Demo

Try the deployed application here: https://autonomous-research-agent-demo.streamlit.app


## Features

- **Web Research:** Uses Tavily Search API to gather relevant information from the web.
- **AI Report Generation:** Uses an LLM through Groq to generate structured research reports.
- **Report Validation:** Validates generated reports and provides feedback.
- **Conditional Retry:** Retries research when validation fails, with a limited retry count.
- **Duplicate Source Filtering:** Avoids adding previously collected URLs during research retries.
- **Checkpointing:** Uses LangGraph SQLite checkpointing to persist workflow state.
- **Markdown Export:** Saves generated research reports as Markdown files.
- **Interactive Web UI:** Built with Streamlit for entering research topics and additional instructions.
- **Real-Time Workflow Integration:** Connects the Streamlit interface to the LangGraph research workflow.
- **Report Display and Download:** Displays generated reports in the browser and allows downloading them as Markdown files.
- **Research Sources:** Displays source links used during research.


## Tech Stack

- Python
- LangGraph
- LangChain
- Groq
- Tavily Search API
- SQLite
- Streamlit 


## Project Structure

```text
autonomous-research-agent/
|-- app.py
|-- main.py
|-- researcher.py
|-- writer.py
|-- validator.py
|-- reports/
|-- requirements.txt
|-- .env
|-- .gitignore
|-- README.md
```


## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/jatinkjain/autonomous-research-agent.git
cd autonomous-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run the agent

```bash
streamlit run app.py
```


## How It Works

1. **Researcher:** Searches the web and collects source titles, URLs, and content.
2. **Writer:** Uses the collected research material to generate a structured report.
3. **Validator:** Checks the generated report and returns validation feedback.
4. **Conditional Routing:** Ends the workflow if validation passes, or retries research when allowed.
5. **Checkpointing:** Stores workflow state using SQLite.
6. **Report Saving:** Writes the generated report to a Markdown file.


## Output

A report can include:

- Executive Summary
- Key Findings
- Analysis
- Limitations and Information Gaps
- Sources


## Current Limitations

- Research quality depends on the available web sources and the language model's output.
- API keys and API usage limits may affect execution.
- Validation does not guarantee that every claim in a report is factually correct.


## Author

JATIN KUMAR JAIN 
