# Job Finder API

An API that scrapes job listings from LinkedIn, Indeed, and Glassdoor, and uses LLM to filter for relevance based on user criteria.

## Features

- Scrapes job listings from multiple sources:
  - LinkedIn
  - Indeed
  - Glassdoor
- Uses OpenAI's GPT to analyze job descriptions for relevance
- Returns structured results in a tabular JSON format
- Beautiful React frontend for searching and viewing job listings

## Backend Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/job-finder-api.git
   cd job-finder-api
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file based on `sample.env`:
   ```
   # Copy the sample.env file to .env
   cp sample.env .env
   # Edit the .env file with your API keys
   ```

4. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Frontend Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

### Backend

1. Start the API server:
   ```
   python run.py
   ```

2. The API will be accessible at: http://localhost:8000

### Frontend

1. Start the React development server:
   ```
   cd frontend
   npm start
   ```

2. The frontend will be accessible at: http://localhost:3000

## API Usage

You can also directly access the API endpoints:

1. Access the API documentation at: http://localhost:8000/docs

2. Make a POST request to the `/api/jobs/search` endpoint with your job search criteria:

```json
{
  "position": "Full Stack Engineer",
  "experience": "2 years",
  "salary": "70,000 PKR to 120,000 PKR",
  "jobNature": "onsite",
  "location": "Peshawar, Pakistan",
  "skills": "full stack, MERN, Node.js, Express.js, React.js, Next.js, Firebase, TailwindCSS, CSS Frameworks, Tokens handling"
}
```

3. Receive a JSON response with relevant job listings:

```json
{
  "relevant_jobs": [
    {
      "job_title": "Full Stack Engineer",
      "company": "XYZ Pvt Ltd",
      "experience": "2+ years",
      "jobNature": "onsite",
      "location": "Islamabad, Pakistan",
      "salary": "100,000 PKR",
      "apply_link": "https://linkedin.com/job123",
      "source": "LinkedIn"
    },
    {
      "job_title": "MERN Stack Developer",
      "company": "ABC Technologies",
      "experience": "2 years",
      "jobNature": "onsite",
      "location": "Lahore, Pakistan",
      "salary": "90,000 PKR",
      "apply_link": "https://indeed.com/job456",
      "source": "Indeed"
    }
  ]
}
```

## Technical Details

### Technologies Used

#### Backend
- **FastAPI**: Web framework for building the API
- **Python**: Core programming language
- **Selenium/BeautifulSoup**: For web scraping job portals
- **OpenAI API**: For analyzing job relevance
- **AsyncIO**: For concurrent job scraping

#### Frontend
- **React**: Frontend library for building UI
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: For making API requests
- **React Toastify**: For displaying notifications

### API Endpoints

- `POST /api/jobs/search`: Search for relevant job listings

### Workflow

1. User fills out job search form with criteria
2. Frontend sends a request to the backend API
3. API concurrently scrapes job listings from multiple sources
4. LLM analyzes and filters jobs based on relevance to the criteria
5. API returns structured results in JSON format
6. Frontend displays the relevant job listings in a user-friendly interface

## License

MIT 