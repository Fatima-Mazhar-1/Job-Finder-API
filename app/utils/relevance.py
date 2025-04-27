import os
from typing import List, Dict, Any
import json
import logging
from openai import OpenAI
from app.api.models import JobListing, JobSearchRequest

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def filter_jobs_by_relevance(jobs: List[JobListing], request: JobSearchRequest) -> List[JobListing]:
    """
    Filter jobs based on relevance using LLM
    """
    if not jobs:
        return []
    
    try:
        # Prepare user criteria
        user_criteria = {
            "position": request.position,
            "experience": request.experience,
            "salary": request.salary,
            "jobNature": request.jobNature,
            "location": request.location,
            "skills": request.skills
        }
        
        # Format jobs list for OpenAI processing
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                "job_title": job.job_title,
                "company": job.company,
                "experience": job.experience or "Not specified",
                "jobNature": job.jobNature or "Not specified",
                "location": job.location or "Not specified",
                "salary": job.salary or "Not specified",
                "source": job.source,
            })
        
        # Create prompt for OpenAI
        prompt = f"""
        I need to identify the most relevant jobs from the following list based on the user's criteria.
        
        User Criteria:
        {json.dumps(user_criteria, indent=2)}
        
        Jobs to Analyze:
        {json.dumps(jobs_data, indent=2)}
        
        For each job, evaluate how well it matches the user's criteria, especially focusing on the following:
        1. Position/job title match
        2. Required experience
        3. Salary expectations (if specified)
        4. Job nature (remote, onsite, hybrid)
        5. Location preference
        6. Required skills
        
        Please return a JSON array containing only the indices of the most relevant jobs from the provided list. 
        The jobs should be ranked by relevance (most relevant first). Only include jobs that are a good match for the user's criteria.
        Format the response as a JSON array like: [0, 5, 2, 9]
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or another suitable model
            messages=[
                {"role": "system", "content": "You are a job matching assistant that helps identify relevant job listings based on specific criteria."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        # Parse response
        try:
            result = json.loads(response.choices[0].message.content)
            relevant_indices = result.get("relevant_indices", [])
            
            if not isinstance(relevant_indices, list):
                logger.error(f"Invalid response format from OpenAI: {response.choices[0].message.content}")
                return jobs[:10]  # Return first 10 jobs as fallback
            
            # Return relevant jobs in order of relevance
            relevant_jobs = []
            for idx in relevant_indices:
                if 0 <= idx < len(jobs):
                    relevant_jobs.append(jobs[idx])
            
            # If no relevant jobs found or invalid response, return top 10
            if not relevant_jobs:
                return jobs[:10]
            
            return relevant_jobs
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing OpenAI response: {e}")
            # Fallback to returning first 10 jobs
            return jobs[:10]
    
    except Exception as e:
        logger.error(f"Error in relevance filtering: {e}")
        # Fallback to returning first 10 jobs
        return jobs[:10] 