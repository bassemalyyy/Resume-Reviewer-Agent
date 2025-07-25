# Resume Reviewer Agent

A resume reviewer and rewriter tool built with CrewAI, Streamlit, and various text extraction libraries. This project helps users improve their resumes and get interview tips based on the job title and the location for the job search.

# Features

Extracts text from PDF and DOCX resume files.
Provides feedback to enhance resume content.
Rewrites resumes to better highlight qualifications.
Offer interview tips for better preparation.
Offers a user-friendly interface via Streamlit.

# Prerequisites

Python 3.10 or higher
Required libraries listed in requirements.txt

# Installation

```sh
git clone https://github.com/bassemalyyy/Resume-Reviewer-Agent.git
```

# Create a virtual environment (optional):

```sh
python -m venv venv
venv\Scripts\activate # On Windows
```

# Install dependencies:

```sh
pip install -r requirements.txt
```

# Set up environment variables:
Set up the API keys using os.enivron[] explicitly in the code.

```sh
SERPER_API_KEY=your_serper_api_key
```

# Usage

Run the Streamlit app:streamlit run resume-review-agent.py
Upload a resume (PDF or DOCX) and enter your preferred location.
Review the feedback, improved resume, and suggested job roles.

# Project Structure
> ├── resume-review-agent.py    # Main application file
> 
> ├── requirements.txt         # Dependency list
> 
> ├── cv-*.docx               # Sample resume files
> 
> ├── Bruce-Wayne-CV.pdf      # Sample PDF resume
> 
> ├── README.md               # This file

# Contributing
Feel free to fork this repository and submit pull requests. Please ensure you follow the existing code style and include tests where applicable.

# License
This project is licensed under the MIT License - see the LICENSE file for details (add a LICENSE file if desired).


# Acknowledgments
CrewAI for the agent framework.
Streamlit for the web interface.
PyMuPDF and Mammoth for document processing.
