# # Warning control
# import warnings
# warnings.filterwarnings('ignore')


# import fitz  # PyMuPDF for PDF processing
# import mammoth  # Mammoth for DOCX to HTML conversion
# import gradio as gr
# import os
# from crewai import Agent, Task, Crew
# from crewai_tools import SerperDevTool
# # from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI


# os.environ["SERPER_API_KEY"] = "241de7455739cd031951b6a94777ee844bb648e4"
# os.environ["GROQ_API_KEY"] = "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"

# # Initialize the LLM with Groq provider and the correct model
# # llm = ChatGroq(
# #     model_name="groq/gemma2-9b-it",  # Use a valid model name for Groq (e.g., llama3-8b-8192 or llama3-70b-8192)
# #     api_key=os.environ["GROQ_API_KEY"],
# # )
# llm = ChatOpenAI(api_key="ollama",model="llama3.2",base_url="http://localhost:11434/v1")

# def extract_text_from_pdf(file_path):
#     """Extracts text from a PDF file using PyMuPDF."""
#     doc = fitz.open(file_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# def extract_text_from_docx(file_path):
#     """Extracts text from a DOCX file using Mammoth for cleaner output."""
#     with open(file_path, "rb") as docx_file:
#         result = mammoth.extract_raw_text(docx_file)
#         return result.value.strip()

# def extract_text_from_resume(file_path):
#     """Determines file type and extracts text."""
#     if file_path.endswith(".pdf"):
#         return extract_text_from_pdf(file_path)
#     elif file_path.endswith(".docx"):
#         return extract_text_from_docx(file_path)
#     else:
#         return "Unsupported file format."



# # Agent 1: Resume Strategist
# resume_feedback = Agent(
#     role="Professional Resume Advisor",
#     goal="Give feedback on the resume to make it stand out in the job market.",
#     verbose=True,
#     backstory="With a strategic mind and an eye for detail, you excel at providing feedback on resumes to highlight the most relevant skills and experiences.",
#     llm=llm,
#     )


# # Task for Resume Strategist Agent: Align Resume with Job Requirements
# resume_feedback_task = Task(
#     description=(
#         """Give feedback on the resume to make it stand out for recruiters. 
#         Review every section, inlcuding the summary, work experience, skills, and education. Suggest to add relevant sections if they are missing.  
#         Also give an overall score to the resume out of 10.  This is the resume: {resume}"""
#     ),
#     expected_output="The overall score of the resume followed by the feedback in bullet points.",
#     agent=resume_feedback
# )

# # Agent 2: Resume Strategist
# resume_advisor = Agent(
#     role="Professional Resume Writer",
#     goal="Based on the feedback recieved from Resume Advisor, make changes to the resume to make it stand out in the job market.",
#     verbose=True,
#     backstory="With a strategic mind and an eye for detail, you excel at refining resumes based on the feedback to highlight the most relevant skills and experiences.",
#     llm=llm
# )

# # Task for Resume Strategist Agent: Align Resume with Job Requirements
# resume_advisor_task = Task(
#     description=(
#         """Rewrite the resume based on the feedback to make it stand out for recruiters. You can adjust and enhance the resume but don't make up facts. 
#         Review and update every section, including the summary, work experience, skills, and education to better reflect the candidates abilities. This is the resume: {resume}"""
#     ),
#     expected_output= "Resume in markdown format that effectively highlights the candidate's qualifications and experiences",
#     # output_file="improved_resume.md",
#     context=[resume_feedback_task],
#     agent=resume_advisor
# )

# search_tool = SerperDevTool()


# # Agent 3: Researcher
# job_researcher = Agent(
#     role = "Senior Recruitment Consultant",
#     goal = "Find the 5 most relevant, recently posted jobs based on the improved resume recieved from resume advisor and the location preference",
#     tools = [search_tool],
#     verbose = True,
#     backstory = """As a senior recruitment consultant your prowess in finding the most relevant jobs based on the resume and location preference is unmatched. 
#     You can scan the resume efficiently, identify the most suitable job roles and search for the best suited recently posted open job positions at the preffered location.""",
#     llm=llm
# )

# research_task = Task(
#     description = """Find the 5 most relevant recent job postings based on the resume recieved from resume advisor and location preference. This is the preferred location: {location} . 
#     Use the tools to gather relevant content and shortlist the 5 most relevant, recent, job openings""",
#     expected_output=(
#         "A bullet point list of the 5 job openings, with the appropriate links and detailed description about each job, in markdown format" 
#     ),
# #    output_file="relevant_jobs.md",
#     agent=job_researcher
# )


# crew = Crew(
#     agents=[resume_feedback, resume_advisor, job_researcher],
#     tasks=[resume_feedback_task, resume_advisor_task, research_task],
#     verbose=True
# )



# def resume_agent(file_path, location):
#     resume_text = extract_text_from_resume(file_path)

#     result = crew.kickoff(inputs={"resume": resume_text, "location": location})

#         # Extract outputs
#     feedback = resume_feedback_task.output.raw.strip("```markdown").strip("```").strip()
#     improved_resume = resume_advisor_task.output.raw.strip("```markdown").strip("```").strip()
#     job_roles = research_task.output.raw.strip("```markdown").strip("```").strip()

#     return feedback, improved_resume, job_roles
        

# # Gradio Interface
# with gr.Blocks() as demo:
#     gr.Markdown("# Resume Feedback and Job Matching Tool")
#     gr.Markdown("*Expected Runtime: 1 Min*")
    
#     with gr.Column():
#         with gr.Row():
#             resume_upload = gr.File(label="Upload Your Resume (PDF or DOCX)", height=120)
#             location_input = gr.Textbox(label="Preferred Location", placeholder="e.g., San Francisco")
#             submit_button = gr.Button("Submit")
        
#         with gr.Column():
#             feedback_output = gr.Markdown(label="Resume Feedback")
#             improved_resume_output = gr.Markdown(label="Improved Resume")
#             job_roles_output = gr.Markdown(label="Relevant Job Roles")

#     # Define the click event for the submit button
#     def format_outputs(feedback, improved_resume, job_roles):
#         # Add bold headings to each section
#         feedback_with_heading = f"## Resume Feedback:**\n\n{feedback}"
#         improved_resume_with_heading = f"## Improved Resume:\n\n{improved_resume}"
#         job_roles_with_heading = f"## Relevant Job Roles:\n\n{job_roles}"
#         return feedback_with_heading, improved_resume_with_heading, job_roles_with_heading



#     submit_button.click(
#         lambda: gr.update(value="Processing..."),
#         inputs=[],
#         outputs=submit_button
#     ).then(
#         resume_agent,
#         inputs=[resume_upload, location_input],
#         outputs=[feedback_output, improved_resume_output, job_roles_output]
#     ).then(
#         format_outputs,
#         inputs=[feedback_output, improved_resume_output, job_roles_output],
#         outputs=[feedback_output, improved_resume_output, job_roles_output]
#     ).then(
#         lambda: gr.update(value="Submit"),
#         inputs=[],
#         outputs=submit_button
#     )

# demo.queue()
# demo.launch(share=True)

import streamlit as st
import fitz  # PyMuPDF for PDF processing
import mammoth  # Mammoth for DOCX to HTML conversion
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import warnings

# Warning control
warnings.filterwarnings('ignore')

# Environment variables
os.environ["SERPER_API_KEY"] = "241de7455739cd031951b6a94777ee844bb648e4"
os.environ["GROQ_API_KEY"] = "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"

# Initialize the LLM
llm = ChatOpenAI(api_key="ollama", model="ollama/llama3.2", base_url="http://localhost:11434/v1")

# File extraction functions
def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file using Mammoth for cleaner output."""
    with open(file_path, "rb") as docx_file:
        result = mammoth.extract_raw_text(docx_file)
        return result.value.strip()

def extract_text_from_resume(file):
    """Determines file type and extracts text."""
    file_path = file.name
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."

# Define Agents and Tasks
resume_feedback = Agent(
    role="Professional Resume Advisor",
    goal="Give feedback on the resume to make it stand out in the job market.",
    verbose=True,
    backstory="With a strategic mind and an eye for detail, you excel at providing feedback on resumes to highlight the most relevant skills and experiences.",
    llm=llm
)

resume_feedback_task = Task(
    description=(
        """Give feedback on the resume to make it stand out for recruiters. 
        Review every section, including the summary, work experience, skills, and education. Suggest to add relevant sections if they are missing.  
        Also give an overall score to the resume out of 10. This is the resume: {resume}"""
    ),
    expected_output="The overall score of the resume followed by the feedback in bullet points.",
    agent=resume_feedback
)

resume_advisor = Agent(
    role="Professional Resume Writer",
    goal="Based on the feedback received from Resume Advisor, make changes to the resume to make it stand out in the job market.",
    verbose=True,
    backstory="With a strategic mind and an eye for detail, you excel at refining resumes based on the feedback to highlight the most relevant skills and experiences.",
    llm=llm
)

resume_advisor_task = Task(
    description=(
        """Rewrite the resume based on the feedback to make it stand out for recruiters. You can adjust and enhance the resume but don't make up facts. 
        Review and update every section, including the summary, work experience, skills, and education to better reflect the candidates abilities. This is the resume: {resume}"""
    ),
    expected_output="Resume in markdown format that effectively highlights the candidate's qualifications and experiences",
    context=[resume_feedback_task],
    agent=resume_advisor
)

search_tool = SerperDevTool()

job_researcher = Agent(
    role="Senior Recruitment Consultant",
    goal="Find the 5 most relevant, recently posted jobs based on the improved resume received from resume advisor and the location preference",
    tools=[search_tool],
    verbose=True,
    backstory="""As a senior recruitment consultant your prowess in finding the most relevant jobs based on the resume and location preference is unmatched. 
    You can scan the resume efficiently, identify the most suitable job roles and search for the best suited recently posted open job positions at the preferred location.""",
    llm=llm
)

research_task = Task(
    description="""Find the 5 most relevant recent job postings based on the resume received from resume advisor and location preference. This is the preferred location: {location}. 
    Use the tools to gather relevant content and shortlist the 5 most relevant, recent, job openings""",
    expected_output="A bullet point list of the 5 job openings, with the appropriate links and detailed description about each job, in markdown format",
    agent=job_researcher
)

crew = Crew(
    agents=[resume_feedback, resume_advisor, job_researcher],
    tasks=[resume_feedback_task, resume_advisor_task, research_task],
    verbose=True
)

# Streamlit UI
st.set_page_config(page_title="Resume Feedback & Job Matching", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stFileUploader {
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 10px;
        color: #FFFFFF;
    }
    .stFileUploader label {
        color: #FFFFFF;
    }
    .stFileUploader div[role="button"] {
        background-color: #2E2E2E;
        color: #FFFFFF;
        border: 1px solid #444;
    }
    .stTextInput>div>input {
        background-color: #2E2E2E;
        border-radius: 8px;
        border: 1px solid #444;
        padding: 8px;
        color: #FFFFFF;
    }
    .stTextInput label {
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Resume Feedback and Job Matching Tool")
st.markdown("*Expected Runtime: ~1 Minute*")

# Input Section
with st.container():
    st.subheader("Upload Your Resume")
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    with col2:
        location = st.text_input("Preferred Location", placeholder="e.g., San Francisco")
    
    submit_button = st.button("Analyze Resume")

# Process and display results
if submit_button:
    if uploaded_file is None:
        st.error("Please upload a resume file.")
    elif not location:
        st.error("Please enter a preferred location.")
    else:
        with st.spinner("Analyzing your resume and finding job matches..."):
            # Save uploaded file temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process resume
            resume_text = extract_text_from_resume(uploaded_file)
            if resume_text == "Unsupported file format.":
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            else:
                result = crew.kickoff(inputs={"resume": resume_text, "location": location})
                
                # Extract outputs
                feedback = resume_feedback_task.output.raw.strip("```markdown").strip("```").strip()
                improved_resume = resume_advisor_task.output.raw.strip("```markdown").strip("```").strip()
                job_roles = research_task.output.raw.strip("```markdown").strip("```").strip()
                
                # Display results
                st.markdown("<div class='section-header'>Resume Feedback</div>", unsafe_allow_html=True)
                st.markdown(feedback, unsafe_allow_html=True)
                
                st.markdown("<div class='section-header'>Improved Resume</div>", unsafe_allow_html=True)
                st.markdown(improved_resume, unsafe_allow_html=True)
                
                st.markdown("<div class='section-header'>Relevant Job Roles</div>", unsafe_allow_html=True)
                st.markdown(job_roles, unsafe_allow_html=True)
                
            # Clean up temporary file
            if os.path.exists("temp_resume.pdf"):
                os.remove("temp_resume.pdf")