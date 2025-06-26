# Resume Reviewer Agent

A resume review and job matching tool built with CrewAI, Streamlit, and various text extraction libraries. This project helps users improve their resumes and find relevant job opportunities based on their skills and preferred location.

# Features

Extracts text from PDF and DOCX resume files.
Provides feedback to enhance resume content.
Rewrites resumes to better highlight qualifications.
Matches users with relevant job postings using web search tools.
Offers a user-friendly interface via Streamlit.

# Prerequisites

Python 3.10 or higher
Required libraries listed in requirements.txt

# Installation

git clone https://github.com/bassemalyyy/Resume-Reviewer-Agent.git


# Create a virtual environment (optional):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


# Install dependencies:

pip install -r requirements.txt


# Set up environment variables:

Create a .env file in the root directory.
Add your API keys:SERPER_API_KEY=your_serper_api_key
GROQ_API_KEY=your_groq_api_key


# Usage

Run the Streamlit app:streamlit run resume-review-agent.py
Upload a resume (PDF or DOCX) and enter your preferred location.
Review the feedback, improved resume, and suggested job roles.

# Project Structure
# ├── resume-review-agent.py    # Main application file
# ├── requirements.txt         # Dependency list
# ├── cv-*.docx               # Sample resume files
# ├── Bruce-Wayne-CV.pdf      # Sample PDF resume
# ├── Resume_Agent_V2_R.ipynb # Jupyter notebook with development notes
# ├── README.md               # This file
# └── .gitignore              # Git ignore file

# Contributing
Feel free to fork this repository and submit pull requests. Please ensure you follow the existing code style and include tests where applicable.
License
This project is licensed under the MIT License - see the LICENSE file for details (add a LICENSE file if desired).
Acknowledgments

CrewAI for the agent framework.
Streamlit for the web interface.
PyMuPDF and Mammoth for document processing.
