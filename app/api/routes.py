from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.api.models import JobSearchRequest, JobSearchResponse, JobListing
from app.scrapers.linkedin import scrape_linkedin_jobs
from app.scrapers.indeed import scrape_indeed_jobs
from app.scrapers.glassdoor import scrape_glassdoor_jobs
from app.utils.relevance import filter_jobs_by_relevance
from typing import List
import asyncio

router = APIRouter()

@router.post("/jobs/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """
    Search for relevant job listings based on provided criteria
    """
    try:
        # Start scraping jobs from different sources concurrently
        linkedin_jobs_task = asyncio.create_task(scrape_linkedin_jobs(request))
        indeed_jobs_task = asyncio.create_task(scrape_indeed_jobs(request))
        glassdoor_jobs_task = asyncio.create_task(scrape_glassdoor_jobs(request))
        
        # Gather results
        results = await asyncio.gather(
            linkedin_jobs_task, 
            indeed_jobs_task,
            glassdoor_jobs_task,
            return_exceptions=True
        )
        
        # Process results, handling any exceptions
        all_jobs = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error scraping jobs: {result}")
                continue
            all_jobs.extend(result)
        
        # Filter jobs by relevance using LLM
        relevant_jobs = await filter_jobs_by_relevance(all_jobs, request)
        
        return JobSearchResponse(relevant_jobs=relevant_jobs)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching for jobs: {str(e)}") 