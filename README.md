# Job-Finder-API
Job Finder API

Job Finder API is a FastAPI-based application designed to help users find and filter relevant job listings based on their personal criteria. It fetches jobs from multiple sources like LinkedIn, Indeed, and a third optional platform such as Google Jobs, Glassdoor, or Rozee.pk. The API processes the job descriptions using Large Language Models (LLMs) and returns only the most relevant opportunities in a structured format.

**About the Project:**

Finding jobs that match a candidate’s specific skills, experience level, salary expectations, and work environment can be difficult. This API aims to solve this by scraping job listings, analyzing their descriptions with AI, and providing a clean, filtered list of the most relevant job opportunities.

**Technologies Used:**

FastAPI for building the REST API Python as the main programming language BeautifulSoup, Selenium, or Scrapy for web scraping Requests or HTTPX for API and website communication OpenAI API, Hugging Face, for LLM-based relevance checking.

**Project Workflow:**

User Input: The client sends a structured JSON request containing job title, experience, salary range, job nature (onsite/remote/hybrid), location, and required skills.

Scraping and Fetching Jobs: The API scrapes job listings from LinkedIn, Indeed, and one optional additional source selected by the developer.

Relevance Filtering: Retrieved job listings are compared with the user’s input using a Large Language Model to check for semantic similarity.

Response: The API returns a JSON output with a list of jobs that are the most relevant based on the input criteria.

**API Input and Output Formats:**

Input Example:

position: Full Stack Engineer experience: 2 years salary: 70,000 PKR to 120,000 PKR jobNature: onsite location: Peshawar, Pakistan skills: full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase, TailwindCSS, CSS Frameworks, Tokens handling

Output Example:

relevant_jobs:

job_title: Full Stack Engineer company: XYZ Pvt Ltd experience: 2+ years jobNature: onsite location: Islamabad, Pakistan salary: 100,000 PKR apply_link: https://linkedin.com/job123

job_title: MERN Stack Developer company: ABC Technologies experience: 2 years jobNature: onsite location: Lahore, Pakistan salary: 90,000 PKR apply_link: https://indeed.com/job456

How Relevance Matching Works:

Instead of simple keyword matching, the API uses Large Language Models like OpenAI GPT or Hugging Face models to semantically analyze job descriptions against the input. The LLM evaluates the following:

Skill match: Checks if the skills required by the job align with user skills

Experience match: Verifies if the candidate’s experience fits the job requirements

Salary match: Compares offered salaries with the expected range

Job nature and location match: Ensures the job nature and location meet user preferences

Only jobs that strongly match across these dimensions are included in the final output.

Running the Project Locally:

Clone the Repository: git clone https://github.com/your-username/job-finder-api.git cd job-finder-api

Create a Virtual Environment: python -m venv venv source venv/bin/activate (for Windows use venv\Scripts\activate)

Install Requirements: pip install -r requirements.txt

Run the Server: uvicorn main:app --reload

Open your browser and go to: http://127.0.0.1:8000/docs

**Deliverables:**

A fully functional FastAPI-based Job Finder API

GitHub Repository with the source code

API documentation.

Sample JSON request and response.

**Notes and Considerations:**

Web scraping on platforms like LinkedIn can be restricted. Whenever possible, prefer using their official APIs. Handle scraping carefully to avoid IP bans by managing rate limits and using user-agents. For deployment, you can use cloud services like Render, Vercel, Railway, or AWS. Keep API keys and sensitive information secure using environment variables.
