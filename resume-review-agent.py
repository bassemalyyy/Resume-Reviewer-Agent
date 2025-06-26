import streamlit as st
import fitz  # PyMuPDF for PDF processing
import mammoth  # Mammoth for DOCX to HTML conversion
import io
import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import warnings

# Warning control
warnings.filterwarnings('ignore')

# Initialize the LLM
llm = ChatOpenAI(api_key="ollama", model="ollama/llama3.2", base_url="http://localhost:11434/v1")

# File extraction functions
def extract_text_from_pdf(file_content):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_content):
    """Extracts text from a DOCX file using Mammoth for cleaner output."""
    result = mammoth.extract_raw_text(io.BytesIO(file_content))
    return result.value.strip()

def extract_text_from_resume(file):
    """Determines file type and extracts text."""
    file_content = file.getvalue()
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file_content)
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

interview_preparation_tips = Agent(
    role="Interview Preparation Expert",
    goal="Provide tailored interview preparation tips based on the job title from the resume and the specified location",
    verbose=True,
    backstory="With extensive experience in career coaching, you excel at crafting interview strategies tailored to specific job roles and regional expectations.",
    llm=llm
)

interview_tips_task = Task(
    description="""Provide tailored interview preparation tips based on the job title extracted from the resume and the specified location. 
    Analyze the resume to determine the candidate's job title or most relevant job role. Offer tips that include common interview questions, preparation strategies, and location-specific advice (e.g., cultural norms or industry trends in {location}). Present the tips in a bullet point list in markdown format. This is the resume: {resume}. This is the preferred location: {location}.""",
    expected_output="A bullet point list of interview preparation tips in markdown format",
    agent=interview_preparation_tips
)

crew = Crew(
    agents=[resume_feedback, resume_advisor, interview_preparation_tips],
    tasks=[resume_feedback_task, resume_advisor_task, interview_tips_task],
    verbose=True
)

# Streamlit UI
st.set_page_config(page_title="Resume Feedback & Interview Prep", layout="wide")

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

st.title("Resume Feedback and Interview Preparation Tool")
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
        with st.spinner("Analyzing your resume and preparing interview tips..."):
            # Process resume directly from uploaded file
            resume_text = extract_text_from_resume(uploaded_file)
            if resume_text == "Unsupported file format.":
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            else:
                result = crew.kickoff(inputs={"resume": resume_text, "location": location})
                
                # Extract outputs
                feedback = resume_feedback_task.output.raw.strip("```markdown").strip("```").strip()
                improved_resume = resume_advisor_task.output.raw.strip("```markdown").strip("```").strip()
                interview_tips = interview_tips_task.output.raw.strip("```markdown").strip("```").strip()
                
                # Display results
                st.markdown("<div class='section-header'>Resume Feedback</div>", unsafe_allow_html=True)
                st.markdown(feedback, unsafe_allow_html=True)
                
                st.markdown("<div class='section-header'>Improved Resume</div>", unsafe_allow_html=True)
                st.markdown(improved_resume, unsafe_allow_html=True)
                
                st.markdown("<div class='section-header'>Interview Preparation Tips</div>", unsafe_allow_html=True)
                st.markdown(interview_tips, unsafe_allow_html=True)
