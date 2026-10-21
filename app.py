import streamlit as st
from main import run_research



st.set_page_config(
    page_title="autonomous research agent",
    layout="wide"
)

st.title("AUTONOMOUS RESEARCH AGENT")

st.write("AI Powered Web Research And Report Generation.")

topic = st.text_input("What Do You Want To Research?",
                      placeholder="Agentic AI Trends in 2026.")

instructions = st.text_area("Additional Research Instructions.(optional)",
                            placeholder="Focus on real-world applications and challenges.")

if st.button("Generate Research Report",type="primary"):
  if not topic.strip():
        st.warning("Please Enter Research Topic.")    
  else:
     try: 
        with st.spinner("Researching, writing, and validating your report..."):
          result = run_research(topic =topic,research_instructions= instructions)

        report = result.get("report","")
        
        if report:
            st.success("Sample report generated!")
            
            st.markdown(report)
            
            st.download_button(
                    label="Download Report",
                    data=report,
                    file_name="research_report.md",
                    mime="text/markdown")

            sources = result.get("sources",[])

            if sources:
                with st.expander("view research sources"):
                    for source in sources:
                        if isinstance(source,dict):
                            title = source.get("title","untitled")
                            url = source.get("url","")
                            st.markdown(f"-[{title} \n {url}]")

        else :
            st.warning("The Agent Did Not Return Report")

     except Exception as e :
         st.error(f"RESEARCH FAILED: {e}")

